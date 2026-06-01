from flask import Blueprint, jsonify, request
from models import Products, get_db, Likes
from routes.auth import checker

products = Blueprint('products', __name__)

@products.route('/api/products/best', methods=['GET'])
def get_best_products():
    try:
        conn = get_db()
        cursor = conn.execute('''
            SELECT id, name, description, price, image_url, category, stock, likes, is_food 
            FROM Product 
            WHERE likes > 0 
            ORDER BY likes DESC 
            LIMIT 3
        ''')
        rows = cursor.fetchall()
        conn.close()
        
        result = [
            {
                'id': row['id'],
                'name': row['name'],
                'description': row['description'],
                'price': row['price'],
                'image': row['image_url'], 
                'category': row['category'],
                'stock': row['stock'],
                'likes': row['likes']
            }
            for row in rows
        ]
        
        print(f"Найдено товаров с лайками: {len(result)}")
        return jsonify({'success': True, 'data': result}), 200
        
    except Exception as e:
        print(f"Ошибка get_best_products: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500

@products.route('/api/products/new-product', methods=['POST'])

@checker
def post_new_product():

    data = request.get_json()
    if not data:
        return jsonify(success=False, error="Данные не были полуены в правильной форме"), 400

    required = ['name', 'description', 'price', 'image_url', 'is_food', 'category', 'stock']
    missing = [f for f in required if not data.get(f)]
    if missing:
        return jsonify(success=False, error=f"Отсутствуют поля: {', '.join(missing)}"), 400

    try:
        pid = Products.create(
            name = data['name'],
            price=float(data['price']),
            image_url=data.get('image_url', ''),
            description=data.get('description', ''),
            is_food=data['is_food'],
            category=data['category'],
            stock=int(data['stock']),
            likes=0 
        )

        newp = Products.get_by_id(pid);

        return jsonify({
            'success': True,
            'data': {
                'id': newp['id'],
                'name': newp['name'],
            }
        }), 201

    except Exception as e:
        return jsonify(success=False, error="Ошибка при создании"), 500

@products.route('/api/products', methods=['GET'])
def get_all_products():
    try:
        all_items = Products.get_all()
        
        data = []
        for item in all_items:
            if not item['is_food']:
                data.append({
                    'id': item['id'],
                    'name': item['name'],
                    'category': item['category'],
                    'description': item['description'],
                    'price': item['price'],
                    'image': item['image_url'],
                    'stock': item['stock'],
                    'likes': item['likes'],
                    'views': item['views']
                })
        
        return jsonify({'success': True, 'data': data}), 200
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return jsonify({'success': False, 'error': str(e)}), 500

@products.route('/api/products/<int:product_id>', methods=['GET'])
def get_single_product(product_id):
    try:
        all_items = Products.get_all()
        product = next((p for p in all_items if p['id'] == product_id), None)
        
        if not product:
            return jsonify({'success': False, 'error': 'Товар не найден'}), 404
        data = {
            'id': product['id'],
            'name': product['name'],
            'category': product['category'],
            'description': product['description'],
            'price': product['price'],
            'image': product['image_url'],
            'stock': product['stock'],
            'likes': product['likes'],
            'views': product['views'],
            'is_food': product['is_food']
        }
        
        return jsonify({'success': True, 'data': data}), 200
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500

@products.route('/api/menu', methods=['GET'])
def get_menu():
    try:
        category = request.args.get('category')
        all_items = Products.get_all()
        
        data = []
        for item in all_items:
            if item['is_food']:
                if category and item['category'] != category:
                    continue
                data.append({
                    'id': item['id'],
                    'name': item['name'],
                    'category': item['category'],
                    'description': item['description'],
                    'price': item['price'],
                    'image': item['image_url'],
                    'stock': item['stock'],
                    'likes': item['likes'],
                    'views': item['views']
                })
        
        return jsonify({'success': True, 'data': data}), 200
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return jsonify({'success': False, 'error': str(e)}), 500

@products.route('/api/menu/categories', methods=['GET'])
def get_menu_categories():
    try:
        all_items = Products.get_all()
        categories = list(set(
            item['category'] for item in all_items if item['is_food']
        ))
        return jsonify({'success': True, 'data': categories}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@products.route('/api/products/<int:product_id>/view', methods=['POST'])
def increment_view(product_id):
    try:
        from models import get_db
        conn = get_db()
        conn.execute('UPDATE Product SET views = views + 1 WHERE id = ?', (product_id,))
        conn.commit()
        conn.close()
        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@products.route('/api/admin/products', methods=['POST'])
@checker
def admin_create_product():
    user = request.current_user
    if user['role'] != 'admin':
        return jsonify({'success': False, 'error': 'Доступ запрещён'}), 403
    
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'error': 'Нет данных'}), 400

    required = ['name', 'price', 'image_url', 'is_food', 'category', 'stock']
    missing = [f for f in required if not data.get(f)]
    if missing:
        return jsonify({'success': False, 'error': f'Отсутствуют поля: {", ".join(missing)}'}), 400
    
    try:
        pid = Products.create(
            name=data['name'].strip(),
            description=data.get('description', '').strip(),
            price=float(data['price']),
            image_url=data['image_url'].strip(),
            is_food=bool(data['is_food']),
            category=data['category'].strip(),
            stock=int(data['stock']),
            likes=0
        )
        new_product = Products.get_by_id(pid)
        return jsonify({
            'success': True,
            'message': 'Товар добавлен',
            'data': {
                'id': new_product['id'],
                'name': new_product['name']
            }
        }), 201
    except Exception as e:
        return jsonify({'success': False, 'error': f'Ошибка сервера: {str(e)}'}), 500


@products.route('/api/admin/products/<int:product_id>', methods=['DELETE'])
@checker
def admin_delete_product(product_id):
    user = request.current_user
    if user['role'] != 'admin':
        return jsonify({'success': False, 'error': 'Доступ запрещён'}), 403
    
    try:
        conn = get_db()
        conn.execute('DELETE FROM Product WHERE id = ?', (product_id,))
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Товар удалён'}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@products.route('/api/admin/products', methods=['GET'])
@checker
def admin_get_products():
    """Получить все товары (для админ-панели)"""
    try:
        user = request.current_user
        if user['role'] != 'admin':
            return jsonify({'success': False, 'error': 'Доступ запрещён'}), 403
        
        all_items = Products.get_all()
        data = [{
            'id': item['id'],
            'name': item['name'],
            'description': item['description'],
            'price': item['price'],
            'image_url': item['image_url'],
            'is_food': item['is_food'],
            'category': item['category'],
            'stock': item['stock'],
            'likes': item['likes'],
            'views': item['views'] if item['views'] is not None else 0
        } for item in all_items]
        
        return jsonify({'success': True, 'data': data}), 200
        
    except Exception as e:
        import traceback, sys
        print(f"\nОШИБКА admin_get_products: {e}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        return jsonify({'success': False, 'error': str(e)}), 500

@products.route('/api/products/<int:product_id>/like', methods=['POST'])
def toggle_like(product_id):
    data = request.get_json()
    user_id = data.get('user_id')
    
    if not user_id:
        return jsonify({"success": False, "message": "Нужна авторизация"}), 401
        
    try:
        is_liked = Likes.toggle(user_id, product_id)
        
        prod = Products.get_by_id(product_id)
        current_likes = prod['likes'] if prod else 0
        
        return jsonify({
            "success": True,
            "is_liked": is_liked,
            "likes": current_likes
        })
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@products.route('/api/products/<int:product_id>/like/status', methods=['GET'])
def get_like_status(product_id):
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"is_liked": False})
        
    is_liked = Likes.get_status(int(user_id), product_id)
    return jsonify({"is_liked": is_liked})