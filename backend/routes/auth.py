from flask import Blueprint, request, jsonify
from models import Users
from config import Config
import jwt
import re
from functools import wraps
import secrets
from datetime import datetime, timedelta

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


def checker(f):
    @wraps(f)
    def joker(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify(success=False, error="Пользователь не авторизован в системе"), 401
        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != 'bearer':
            return jsonify(success=False, error="Неверный формат"), 403
        token = parts[1]
        try:
            payload = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return jsonify(success=False, error="Срок токена истёк"), 401
        except jwt.InvalidTokenError:
            return jsonify(success=False, error="Невалидный токен"), 403
        user = Users.find_by_id(payload['user_id'])
        if not user:
            return jsonify(success=False, error="Пользователь не найден"), 404
        if request.endpoint and 'admin' in request.endpoint:
            if user['role'] != 'admin':
                return jsonify(success=False, error="Требуется роль администратора"), 403
        
        request.current_user = user
        return f(*args, **kwargs)
    return joker


def generate_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(hours=Config.TOKEN_EXPIRY_HOURS)
    }
    return jwt.encode(payload, Config.SECRET_KEY, algorithm='HS256')

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data:
        return jsonify({'message': 'Нет данных'}), 400

    email = data.get('email')
    password = data.get('password')

    if not all([email, password]):
        return jsonify({'message': 'Все поля обязательны'}), 400

    user = Users.find_by_email(email)

    if not user:
        return jsonify({'message': 'Почта пользователя не найдена'}), 404

    if not Users.verify_password(user['password_hash'], password):
        return jsonify({'message': 'Неверный пароль'}), 401

    token = generate_token(user['id'])

    return jsonify({
        'token': token,
        'user': {
            'id': user['id'],
            'email': user['email'],
            'username': user['username'],
            'role': user['role']
        }
    }), 200

@auth_bp.route('/me', methods=['GET'])
@checker
def me():
    get_me = request.current_user
    return jsonify({
        'success': True,
        'data': {
            'id': get_me['id'],
            'name': get_me['username'],
            'email': get_me['email'],
            'createdAt': get_me['created_at'],
            'role': get_me['role']
        }
    }), 200

# @auth_bp.route('/register', methods=['POST'])
# def register():
#     data = request.get_json()
    
#     if not data:
#         return jsonify({'success': False, 'message': 'Нет данных'}), 400
    
#     email = data.get('email')
#     password = data.get('password')
#     username = data.get('username')
    
#     if not all([email, password, username]):
#         return jsonify({'success': False, 'message': 'Все поля обязательны'}), 400
    
#     if not validate_email(email):
#         return jsonify({'success': False, 'message': 'Некорректный email'}), 400
    
#     if len(password) < 6:
#         return jsonify({'success': False, 'message': 'Пароль должен содержать минимум 6 символов'}), 400
#     if Users.find_by_email(email):
#         return jsonify({'success': False, 'message': 'Пользователь с таким email уже существует'}), 409
    
#     try:
#         user_id = Users.create(
#             email=email,
#             username=username,
#             password=password,
#             role='user'
#         )
        
#         token = generate_token(user_id)
#         new_user = Users.find_by_id(user_id)
        
#         return jsonify({
#             'success': True,
#             'message': 'Регистрация успешна',
#             'token': token,
#             'user': {
#                 'id': new_user['id'],
#                 'email': new_user['email'],
#                 'username': new_user['username'],
#                 'role': new_user['role']
#             }
#         }), 201
        
#     except Exception as e:
#         return jsonify({'success': False, 'message': f'Ошибка сервера: {str(e)}'}), 500

@auth_bp.route('/register', methods=['POST'])
def register():
    import traceback
    try:
        data = request.get_json()
        email = data.get('email', '').strip()
        username = data.get('username', '').strip()
        password = data.get('password', '')

        print(f"📥 Попытка регистрации: email={email}, user={username}")

        if not all([email, username, password]):
            return jsonify({'error': 'Все поля обязательны'}), 400

        if len(password) < 6:
            return jsonify({'error': 'Пароль минимум 6 символов'}), 400

        if Users.find_by_email(email):
            return jsonify({'error': 'Email уже занят'}), 409

        # Создаём пользователя
        user_id = Users.create(email, username, password)
        print(f"✅ Пользователь создан, ID: {user_id}")
        
        # Генерируем токен
        token = generate_token(user_id)
        user = Users.find_by_id(user_id)

        return jsonify({
            'success': True,
            'token': token,
            'user': {
                'id': user['id'],
                'email': user['email'],
                'username': user['username'],
                'role': user['role']
            }
        }), 201
        
    except Exception as e:
        print("\n🔥🔥🔥 ТОЧНАЯ ОШИБКА БЭКЕНДА:")
        traceback.print_exc()  # ← Выведет полный стек ошибки в консоль
        return jsonify({'error': 'Внутренняя ошибка сервера'}), 500
        
@auth_bp.route('/recovery/keyword', methods=['POST'])
@checker
def set_recovery_keyword():
    try:
        user_id = request.current_user['id']
        data = request.get_json()
        keyword = data.get('keyword', '').strip()
        
        if len(keyword) < 4:
            return jsonify({'error': 'Секретное слово должно быть минимум 4 символа'}), 400
        
        success = Users.set_recovery_keyword(user_id, keyword)
        if success:
            return jsonify({'success': True, 'message': 'Секретное слово сохранено'}), 200
        return jsonify({'error': 'Не удалось сохранить'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/recovery/verify-keyword', methods=['POST'])
def verify_recovery_keyword():
    try:
        data = request.get_json()
        email = data.get('email', '').lower().strip()
        keyword = data.get('keyword', '').strip()
        
        if not email or not keyword:
            return jsonify({'error': 'Email и секретное слово обязательны'}), 400
        
        result = Users.verify_recovery_keyword(email, keyword)
        
        if result['success']:
            reset_token = secrets.token_urlsafe(32)
            return jsonify({
                'success': True,
                'reset_token': reset_token,
                'user_id': result['user_id']
            }), 200
        else:
            return jsonify({'error': result.get('error', 'Неверные данные')}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/recovery/reset', methods=['POST'])
def reset_password():
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        new_password = data.get('new_password', '').strip()
        
        if not user_id or not new_password:
             return jsonify({'error': 'ID пользователя и пароль обязательны'}), 400

        if len(new_password) < 6:
            return jsonify({'error': 'Пароль должен быть минимум 6 символов'}), 400
        
        success = Users.update_password(user_id, new_password)
        
        if success:
            return jsonify({'success': True, 'message': 'Пароль успешно изменён'}), 200
        return jsonify({'error': 'Не удалось обновить пароль'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500