from flask import Blueprint, request, jsonify
from models import Cart
from routes.auth import checker as token_required

cart_bp = Blueprint('cart', __name__, url_prefix='/api')

@cart_bp.route('/cart', methods=['GET'])
@token_required
def get_cart():
    user_id = request.current_user['id']
    items = Cart.get_user_cart(user_id)
    return jsonify({
        'items': [{
            'id': i['cart_id'], 'product_id': i['product_id'],
            'name': i['name'], 'price': i['price'],
            'quantity': i['quantity'], 'image': i['image_url']
        } for i in items]
    })

@cart_bp.route('/cart', methods=['POST'])
@token_required
def add_to_cart():
    user_id = request.current_user['id']
    data = request.get_json()
    if not data or 'product_id' not in data:
        return jsonify({'error': 'product_id обязателен'}), 400
    Cart.add_item(user_id, data['product_id'], data.get('quantity', 1))
    return jsonify({'success': True}), 201

@cart_bp.route('/cart/<int:product_id>', methods=['PUT'])
@token_required
def update_cart_item(product_id):
    user_id = request.current_user['id']
    quantity = request.get_json().get('quantity', 1)
    Cart.update_quantity(user_id, product_id, quantity)
    return jsonify({'success': True})

@cart_bp.route('/cart/<int:product_id>', methods=['DELETE'])
@token_required
def remove_from_cart(product_id):
    user_id = request.current_user['id']
    Cart.remove_item(user_id, product_id)
    return jsonify({'success': True})

@cart_bp.route('/cart', methods=['DELETE'])
@token_required
def clear_cart():
    user_id = request.current_user['id']
    Cart.clear_cart(user_id)
    return jsonify({'success': True})

@cart_bp.route('/cart/<int:product_id>/check', methods=['GET'])
@token_required
def check_in_cart(product_id):
    """Проверить, есть ли товар в корзине пользователя"""
    user_id = request.current_user['id']
    try:
        items = Cart.get_user_cart(user_id)
        # Ищем товар по product_id в списке корзины
        in_cart = any(item['product_id'] == product_id for item in items)
        return jsonify({'in_cart': in_cart})
    except Exception as e:
        return jsonify({'error': str(e)}), 500