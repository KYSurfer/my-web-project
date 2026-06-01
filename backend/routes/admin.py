from flask import Blueprint, request, jsonify
from models import get_db
from routes.auth import checker  

admin_bp = Blueprint('admin', __name__, url_prefix='/api')

@admin_bp.route('/admin/users', methods=['GET'])
@checker
def get_users():
    """Получить список всех пользователей (только для админов)"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, email, username, role, created_at 
            FROM User 
            ORDER BY created_at DESC
        ''')
        rows = cursor.fetchall()
        conn.close()
        users_list = []
        for row in rows:
            users_list.append({
                'id': row['id'],
                'email': row['email'],
                'username': row['username'],
                'role': row['role'],
                'created_at': row['created_at']
            })

        return jsonify(success=True, data=users_list)
    
    except Exception as e:
        print(f"❌ Ошибка get_users: {e}")
        return jsonify(success=False, error=str(e)), 500

@admin_bp.route('/admin/users/<int:user_id>', methods=['DELETE'])
@checker
def delete_user(user_id):
    """Удалить пользователя по ID (только для админов)"""
    try:
        if request.current_user['id'] == user_id:
            return jsonify(success=False, error="Нельзя удалить самого себя"), 400
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM User WHERE id = ?', (user_id,))
        conn.commit()
        
        deleted = cursor.rowcount > 0
        conn.close()
        
        if deleted:
            return jsonify(success=True, message="Пользователь удалён")
        else:
            return jsonify(success=False, error="Пользователь не найден"), 404
    
    except Exception as e:
        print(f"❌ Ошибка delete_user: {e}")
        return jsonify(success=False, error=str(e)), 500


@admin_bp.route('/admin/stats', methods=['GET'])
@checker
def get_stats():
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) as count FROM User')
        users_count = cursor.fetchone()['count']
        
        cursor.execute('SELECT COUNT(*) as count FROM Product')
        products_count = cursor.fetchone()['count']
        
        cursor.execute('SELECT COUNT(*) as count FROM "Order"')
        orders_count = cursor.fetchone()['count']
        
        conn.close()
        
        return jsonify(
            success=True,
            data={"users": users_count, "products": products_count, "orders": orders_count}
        )
    except Exception as e:
        return jsonify(success=False, error=str(e)), 500