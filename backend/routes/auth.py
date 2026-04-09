from flask import Blueprint, request, jsonify
from models import Users
from config import Config
import jwt
import re
import datetime
from functools import wraps

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
        request.current_user = user
        return f(*args, **kwargs)
    return joker


def generate_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=Config.TOKEN_EXPIRY_HOURS)
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
            'username': user['username']
        }
    }), 200


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    if not data:
        return jsonify({'message': 'Не получилось зарегистрироваться'}), 400

    email = data.get('email')
    password = data.get('password')
    username = data.get('username')

    if not all([email, password, username]):
        return jsonify({'message': 'Все поля обязательны'}), 400

    if not validate_email(email):
        return jsonify({'message': 'Неверный формат почты'}), 400

    if len(password) < 6:
        return jsonify({'message': 'Длина пароля должна быть более 6 символов'}), 400

    exist = Users.find_by_email(email)

    if exist:
        return jsonify({'message': 'Пользователь с такой почтой существует'}), 400

    user_id = Users.create(email, username, password)

    token = generate_token(user_id)

    return jsonify({
        'token': token,
        'user': {
            'id': user_id,
            'email': email,
            'username': username
        }
    }), 201

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
            'createdAt': get_me['created_at']
        }
    }), 200