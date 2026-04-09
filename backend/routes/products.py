from flask import Blueprint, jsonify, request
from models import Products
from routes.auth import checker

products = Blueprint('products', __name__)

@products.route('/api/products/best', methods=['GET'])

def get_best_products():

    try:
        best_products = Products.get_best_by_likes(limit=3)

        result = [{
            'id': p['id'],
            'name': p['name'],
            'price': p['price'],
            'image': p['image_url'],
            'likes': p['likes'],
            'description': p['description'],
            'category': p['category'],
            'stock': p['stock']
        } for p in best_products]

        return jsonify({
            'success': True,
            'data':result
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error':str(e)
        }), 500

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