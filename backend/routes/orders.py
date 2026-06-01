from flask import Blueprint, request, jsonify
from models import Orders, Cart
from routes.auth import checker as token_required

orders_bp = Blueprint('orders', __name__, url_prefix='/api')

@orders_bp.route('/orders', methods=['GET'])
@token_required
def get_orders():
    user_id = request.current_user['id']
    orders = Orders.get_user_orders(user_id)
    return jsonify({'data': orders})

@orders_bp.route('/orders', methods=['POST'])
@token_required
def create_order():
    user_id = request.current_user['id']
    data = request.get_json()
    items = data.get('items', [])
    if not items:
        return jsonify({'error': 'Корзина пуста'}), 400
    success = Orders.create_order(user_id, items)
    if success:
        Cart.clear_cart(user_id)
        return jsonify({'success': True}), 201
    return jsonify({'error': 'Заказ оформлен'}), 400