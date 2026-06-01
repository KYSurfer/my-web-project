from flask import Blueprint, jsonify

characters_bp = Blueprint('characters', __name__)
BASE_URL = "http://localhost:5000"

CHARACTERS_DATA = [
    {
        "id": 1,
        "title": "Бон, Кролик",
        "name": "«Бон»",
        "image": f"{BASE_URL}/static/images/bon-info.jpg",
        "alt": "Bon the Rabbit",
        "route": "/character/bon",
        "role": "Легенда ресторана",
        "summary": "Бон — это сердце и душа Bon's Burgers! Наш любимый пушистый друг с фирменной улыбкой всегда готов обнять каждого гостя. Он верит, что каждый посетитель особенный, и хранит память о каждом визите навсегда. Приходите познакомиться с тем, кто никогда не забывает ваши лица!",
        "bio": """
            <p><strong>Бон</strong> — это не просто аниматроник, это душа самого Bon's Burgers! Наш пушистый талисман с фирменным галстуком-бабочкой стал символом радости для тысяч семей.</p>
            
            <h3>История создания</h3>
            <p>Бон был разработан в начале 80-х как центральный персонаж шоу. Его дизайн вдохновлён классическими мультфильмами: большие выразительные глаза, дружелюбная улыбка и мягкие формы создают образ идеального друга для детей.</p>
            
            <h3>Характер</h3>
            <p>Бон обожает внимание, игры и объятия. Он всегда в центре событий: поёт, танцует и дарит улыбки. Его девиз: «Каждый гость — особенный!»</p>
        """,
        "firstAppearance": "Август 2021 (findjackwalten.com)",
        "creator": "Джек Уолтен",
        "voiceActor": "Неизвестно",
        "stats": {"danger": "10/10", "intelligence": "9/10", "mystery": "10/10", "strength": "8/10"},
        "gallery": [
            f"{BASE_URL}/static/images/bon-gallery-1.jpg",
            f"{BASE_URL}/static/images/bon-gallery-2.jpg",
            f"{BASE_URL}/static/images/bon-gallery-3.jpg"
        ],
        "related": [
            {"id": 2, "name": "Ша", "image": f"{BASE_URL}/static/images/sha-thumb.jpg"},
            {"id": 3, "name": "Бузу", "image": f"{BASE_URL}/static/images/boozoo-thumb.jpg"}
        ]
    },
    {
        "id": 2,
        "title": "Ша, Овечка",
        "name": "«Ша»",
        "image": f"{BASE_URL}/static/images/sha-info.jpg",
        "alt": "Sha the Sheep",
        "route": "/character/sha",
        "role": "Аниматроник-овечка",
        "summary": "Ша — музыкальная душа Bon's Burgers, очаровательная овечка с голосом, который покоряет сердца.",
        "bio": """
            <p><strong>Ша</strong> — наша звёздная певица и главная хранительница мелодий! Её нежный голос и зажигательные танцы делают каждое шоу незабываемым.</p>
            
            <h3>Талант</h3>
            <p>Ша владеет уникальной вокальной техникой, способной тронуть до слёз. Её репертуар включает как весёлые детские песенки, так и трогательные баллады.</p>
            
            <h3>Личность</h3>
            <p>Добрая, заботливая и немного застенчивая, Ша всегда поддерживает друзей и создаёт тёплую атмосферу в ресторане.</p>
        """,
        "firstAppearance": "2021",
        "creator": "Джек Уолтен",
        "voiceActor": "Неизвестно",
        "knownFor": ["Певица", "Хранительница мелодий", "Друг Бона"],
        "images": [{"url": f"{BASE_URL}/static/images/sha-info.jpg", "label": "Основное"}],
        "stats": {"danger": "3/10", "intelligence": "7/10", "speed": "8/10", "charm": "10/10"},
        "gallery": [f"{BASE_URL}/static/images/sha-gallery-1.jpg", f"{BASE_URL}/static/images/sha-gallery-2.jpg"],
        "related": [
            {"id": 1, "name": "Бон", "image": f"{BASE_URL}/static/images/bon-thumb.jpg"},
            {"id": 4, "name": "Банни", "image": f"{BASE_URL}/static/images/bunny-thumb.jpg"}
        ]
    },
    {
        "id": 3,
        "title": "Бузу, Шоумастер",
        "name": "«Бузу»",
        "image": f"{BASE_URL}/static/images/boozoo-info.jpg",
        "alt": "Boozoo",
        "route": "/character/boozoo",
        "role": "Шоумастер",
        "summary": "Бузу — энергичный шоумен в красном пиджаке, мастер фокусов и неиссякаемый источник веселья.",
        "bio": """
            <p><strong>Бузу</strong> — наш харизматичный ведущий и король интерактива! Этот клоун в стильном пиджаке знает, как зажечь публику.</p>
            
            <h3>Шоу-программа</h3>
            <p>Бузу сочетает комедию, магию и танцы в одном выступлении. Его фирменные фокусы с исчезновением и появлением предметов приводят в восторг детей и взрослых.</p>
            
            <h3>Особенности</h3>
            <p>Бузу обожает сюрпризы и всегда подходит к столикам гостей, чтобы подарить маленький сувенир или рассказать анекдот.</p>
        """,
        "firstAppearance": "2021",
        "creator": "Джек Уолтен",
        "voiceActor": "Неизвестно",
        "knownFor": ["Шоумен", "Мастер фокусов", "Король интерактива"],
        "images": [{"url": f"{BASE_URL}/static/images/boozoo-info.jpg", "label": "Основное"}],
        "stats": {"danger": "6/10", "intelligence": "8/10", "speed": "7/10", "charm": "10/10"},
        "gallery": [f"{BASE_URL}/static/images/boozoo-gallery-1.jpg"],
        "related": [
            {"id": 1, "name": "Бон", "image": f"{BASE_URL}/static/images/bon-thumb.jpg"},
            {"id": 5, "name": "Билли", "image": f"{BASE_URL}/static/images/billy-thumb.jpg"}
        ]
    },
    {
        "id": 4,
        "title": "Банни, Крольчиха",
        "name": "«Банни»",
        "image": f"{BASE_URL}/static/images/bunny-info.jpg",
        "alt": "Banny",
        "route": "/character/banny",
        "role": "Элегантная леди",
        "summary": "Банни — элегантная крольчиха, воплощение стиля и грации в мире аниматроников Bon's Burgers.",
        "bio": """
            <p><strong>Банни</strong> — наша утончённая леди с безупречным вкусом! Её изящные движения и аристократичная манера речи делают её фавориткой публики.</p>
            
            <h3>Стиль</h3>
            <p>Банни всегда в идеальном наряде: от классического платья до праздничного костюма. Она вдохновляет гостей на творчество и самовыражение.</p>
            
            <h3>Характер</h3>
            <p>Спокойная, мудрая и немного загадочная, Банни наблюдает за всем с лёгкой улыбкой. Она — тихая сила, которая объединяет команду.</p>
        """,
        "firstAppearance": "2021",
        "creator": "Джек Уолтен",
        "voiceActor": "Неизвестно",
        "knownFor": ["Стиль", "Грация", "Загадочность"],
        "images": [{"url": f"{BASE_URL}/static/images/bunny-info.jpg", "label": "Основное"}],
        "stats": {"danger": "4/10", "intelligence": "9/10", "elegance": "10/10", "mystery": "8/10"},
        "gallery": [f"{BASE_URL}/static/images/bunny-gallery-1.jpg"],
        "related": [
            {"id": 1, "name": "Бон", "image": f"{BASE_URL}/static/images/bon-thumb.jpg"},
            {"id": 2, "name": "Ша", "image": f"{BASE_URL}/static/images/sha-thumb.jpg"}
        ]
    },
    {
        "id": 5,
        "title": "Билли, Клоун",
        "name": "«Билли»",
        "image": f"{BASE_URL}/static/images/billy-info.jpg",
        "alt": "Billy",
        "route": "/character/billy",
        "role": "Клоун-комик",
        "summary": "Билли — весёлый клоун с безграничной энергией, который превращает каждый день в праздник смеха.",
        "bio": """
            <p><strong>Билли</strong> — наш главный комик и мастер импровизации! Его яркий грим, смешные выходки и заразительный хохот гарантируют хорошее настроение.</p>
            
            <h3>Развлечения</h3>
            <p>Билли специализируется на физических комедиях, жонглировании и интерактивных играх с залом. Он всегда находит подход к самому застенчивому гостю.</p>
            
            <h3>Философия</h3>
            <p>«Смех — лучшее лекарство!» — говорит Билли. И он делает всё, чтобы каждый уходил из Bon's Burgers с улыбкой.</p>
        """,
        "firstAppearance": "2021",
        "creator": "Джек Уолтен",
        "voiceActor": "Неизвестно",
        "knownFor": ["Комедия", "Импровизация", "Неиссякаемый смех"],
        "images": [{"url": f"{BASE_URL}/static/images/billy-info.jpg", "label": "Основное"}],
        "stats": {"danger": "5/10", "intelligence": "6/10", "speed": "9/10", "humor": "10/10"},
        "gallery": [f"{BASE_URL}/static/images/billy-gallery-1.jpg"],
        "related": [
            {"id": 3, "name": "Бузу", "image": f"{BASE_URL}/static/images/boozoo-thumb.jpg"},
            {"id": 6, "name": "Рокета", "image": f"{BASE_URL}/static/images/rocket-thumb.jpg"}
        ]
    },
    {
        "id": 6,
        "title": "Рокета, Игрушка",
        "name": "«Рокета»",
        "image": f"{BASE_URL}/static/images/rocket-info.png",
        "alt": "Rocket",
        "route": "/character/rocket",
        "role": "Космический исследователь",
        "summary": "Рокета — космический мечтатель в мире аниматроников, вдохновляющий детей на большие открытия.",
        "bio": """
            <p><strong>Рокета</strong> — наш звёздный исследователь и популяризатор науки! Этот очаровательный робот-игрушка делает обучение увлекательным приключением.</p>
            
            <h3>Миссия</h3>
            <p>Рокета рассказывает о космосе, технологиях и чудесах науки через игры и эксперименты. Его интерактивные шоу пробуждают любопытство и воображение.</p>
            
            <h3>Особенности</h3>
            <p>Рокета говорит на «языке будущего»: простые объяснения сложных концепций, яркие визуальные эффекты и интерактивные элементы.</p>
        """,
        "firstAppearance": "2021",
        "creator": "Джек Уолтен",
        "voiceActor": "Неизвестно",
        "knownFor": ["Наука", "Космос", "Интерактивные шоу"],
        "images": [{"url": f"{BASE_URL}/static/images/rocket-info.png", "label": "Основное"}],
        "stats": {"danger": "2/10", "intelligence": "10/10", "speed": "5/10", "creativity": "10/10"},
        "gallery": [f"{BASE_URL}/static/images/rocket-gallery-1.jpg"],
        "related": [
            {"id": 5, "name": "Билли", "image": f"{BASE_URL}/static/images/billy-thumb.jpg"},
            {"id": 8, "name": "Кибертелли", "image": f"{BASE_URL}/static/images/cybertelly-thumb.jpg"}
        ]
    },
    {
        "id": 7,
        "title": "Сноубеар, Соня",
        "name": "«Сноубеар»",
        "image": f"{BASE_URL}/static/images/snowbear-info.jpg",
        "alt": "Snowbear",
        "route": "/character/snowbear",
        "role": "Хранитель уюта",
        "summary": "Сноубеар — уютный полярный мишка, создающий атмосферу тепла и комфорта в любое время года.",
        "bio": """
            <p><strong>Сноубеар</strong> — наш пушистый хранитель уюта! Этот добродушный мишка создаёт ощущение домашнего очага в самом сердце ресторана.</p>
            
            <h3>Атмосфера</h3>
            <p>Сноубеар обожает тихие беседы, тёплые истории и спокойные игры. Его зона — идеальное место, чтобы отдохнуть от шума и суеты.</p>
            
            <h3>Характер</h3>
            <p>Медлительный, мудрый и невероятно терпеливый, Сноубеар выслушает любого и всегда найдёт нужные слова поддержки.</p>
        """,
        "firstAppearance": "2021",
        "creator": "Джек Уолтен",
        "voiceActor": "Неизвестно",
        "knownFor": ["Уют", "Терпение", "Тёплые истории"],
        "images": [{"url": f"{BASE_URL}/static/images/snowbear-info.jpg", "label": "Основное"}],
        "stats": {"danger": "1/10", "intelligence": "7/10", "strength": "8/10", "warmth": "10/10"},
        "gallery": [f"{BASE_URL}/static/images/snowbear-gallery-1.jpg"],
        "related": [
            {"id": 2, "name": "Ша", "image": f"{BASE_URL}/static/images/sha-thumb.jpg"},
            {"id": 4, "name": "Банни", "image": f"{BASE_URL}/static/images/bunny-thumb.jpg"}
        ]
    },
    {
        "id": 8,
        "title": "Кибертелли",
        "name": "«Кибертелли»",
        "image": f"{BASE_URL}/static/images/real-cybertelly-infov=2.jpg",
        "alt": "Cybertelly",
        "route": "/character/cybertelly",
        "role": "Цифровой ведущий",
        "summary": "Кибертелли — футуристический ведущий, объединяющий технологии и развлечения в уникальном цифровом опыте.",
        "bio": """
            <p><strong>Кибертелли</strong> — наш инновационный гид в мире цифровых развлечений! Этот высокотехнологичный аниматроник представляет будущее шоу-бизнеса уже сегодня.</p>
            
            <h3>Технологии</h3>
            <p>Кибертелли использует передовые проекции, интерактивные экраны и адаптивный контент, чтобы каждое выступление было уникальным и персонализированным.</p>
            
            <h3>Контент</h3>
            <p>От образовательных программ до развлекательных викторин — Кибертелли делает информацию доступной и увлекательной для всех возрастов.</p>
        """,
        "firstAppearance": "2021",
        "creator": "Джек Уолтен",
        "voiceActor": "Неизвестно",
        "knownFor": ["Технологии", "Интерактив", "Будущее развлечений"],
        "images": [{"url": f"{BASE_URL}/static/images/real-cybertelly-infov=2.jpg", "label": "Основное"}],
        "stats": {"danger": "7/10", "intelligence": "10/10", "speed": "6/10", "tech": "10/10"},
        "gallery": [f"{BASE_URL}/static/images/cybertelly-gallery-1.jpg"],
        "related": [
            {"id": 6, "name": "Рокета", "image": f"{BASE_URL}/static/images/rocket-thumb.jpg"},
            {"id": 1, "name": "Бон", "image": f"{BASE_URL}/static/images/bon-thumb.jpg"}
        ]
    }
]

@characters_bp.route('/api/characters', methods=['GET'])
def get_characters():
    """Возвращает базовый список для карточек"""
    return jsonify({"success": True, "data": CHARACTERS_DATA})

@characters_bp.route('/api/characters/<character_id>', methods=['GET'])
def get_character(character_id):
    """Возвращает полные данные персонажа для страницы (Вики-формат)"""
    try:
        character = None
        if character_id.isdigit():
            character = next((c for c in CHARACTERS_DATA if c['id'] == int(character_id)), None)
        
        if not character:
            target_route = f'/character/{character_id}'
            character = next((c for c in CHARACTERS_DATA if c.get('route') == target_route), None)
        
        if not character:
            return jsonify({
                "success": False, 
                "message": f"Персонаж '{character_id}' не найден"
            }), 404
        
        full_character = {
            "id": character['id'],
            "name": character.get('name') or character.get('title', 'Unknown'),
            "role": character.get('role', 'Персонаж'),
            "summary": character.get('summary', 'Описание персонажа...'),
            
            "bio": character.get('bio', '<p>Биография...</p>'),
            "firstAppearance": character.get('firstAppearance', '2021'),
            "creator": character.get('creator'),
            "knownFor": character.get('knownFor', []),
            "images": character.get('images', [{"url": character.get('image'), "label": "Основное"}]),
            "image": character.get('image'),
            "stats": character.get('stats', {}),
            "related": character.get('related', [])
        }
        
        return jsonify({"success": True, "data": full_character})
    
    except Exception as e:
        print(f"❌ Ошибка в get_character: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"success": False, "message": f"Server error: {str(e)}"}), 500