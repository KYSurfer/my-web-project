from flask import Blueprint, jsonify, request
from models import Products

from routes.cast import CAST_DATA
from routes.characters import CHARACTERS_DATA

search_bp = Blueprint('search', __name__)

@search_bp.route('/api/search', methods=['GET'])
def global_search():
    query = request.args.get('q', '').strip().lower()
    
    if not query:
        return jsonify([])

    results = []

    try:
        all_products = Products.get_all()
        for item in all_products:
            name = (item['name'] or '').lower()
            desc = (item['description'] or '').lower()
            
            if query in name or query in desc:
                results.append({
                    'id': f"prod_{item['id']}",
                    'title': item['name'],
                    'image': item['image_url'],
                    'type': 'menu' if item['is_food'] else 'merch',
                    'type_label': 'Меню' if item['is_food'] else 'Товары',
                    'route': '/menu' if item['is_food'] else '/merch'
                })
    except Exception as e:
        print(f"Ошибка поиска в БД: {e}")

    for member in CAST_DATA:
        title = (member.get('title') or '').lower()
        if query in title:
            results.append({
                'id': f"cast_{member['id']}",
                'title': member['title'],
                'image': member.get('image'),
                'type': 'cast',
                'type_label': 'Персонал',
                'route': member.get('route', '/cast')
            })

    for char in CHARACTERS_DATA:
        title = (char.get('title') or '').lower()
        if query in title:
            results.append({
                'id': f"char_{char['id']}",
                'title': char['title'],
                'image': char.get('image'),
                'type': 'star',
                'type_label': 'Аниматроник',
                'route': char.get('route', '/stars')
            })

    return jsonify(results[:8])