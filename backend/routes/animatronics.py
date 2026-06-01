from flask import Blueprint, jsonify

animatronics_bp = Blueprint('animatronics', __name__)

BASE_URL = "http://localhost:5000"

@animatronics_bp.route('/api/animatronics', methods=['GET'])
def get_animatronics():
    data = [
        {
            "id": 1,
            "name": "Bon the Rabbit",
            "alias": "►►Главный Маскот",
            "description": "Синий кролик-аниматроник и главный талисман Bon's Burgers. Лицо ресторана.",
            "image": f"{BASE_URL}/static/images/bon-frontpage.jpg",
            "route": "/animatronic/bon"
        },
        {
            "id": 2,
            "name": "Banny the Hare",
            "alias": "►►Веселая зайчиха",
            "description": "Фиолетовый кролик-аниматроник, сестра Бона. Известна своим музыкальным талантом.",
            "image": f"{BASE_URL}/static/images/banny-frontpage.png",
            "route": "/animatronic/banny"
        },
        {
            "id": 3,
            "name": "Sha the Sheep",
            "alias": "►►Милая овечка",
            "description": "Овца-аниматроник с пушистой шерстью. Добрая душа группы.",
            "image": f"{BASE_URL}/static/images/Sha-frontpage.jpg",
            "route": "/animatronic/sha"
        },
        {
            "id": 4,
            "name": "Boozoo the Showmaster",
            "alias": "►►Лучший ведущий",
            "description": "Аниматроник с магическими способностями и в красной куртке.",
            "image": f"{BASE_URL}/static/images/boozoo-frontpage.jpg",
            "route": "/animatronic/boozoo"
        }
    ]
    return jsonify({"success": True, "data": data})