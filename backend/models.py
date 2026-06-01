import sqlite3
import hashlib
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config

def get_db():
    connection = sqlite3.connect(Config.DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection

def init_db():
    try:
        conn.execute("ALTER TABLE User ADD COLUMN recovery_keyword_hash TEXT")
    except Exception:
        pass

    conn = get_db()
    conn.execute('''
    CREATE TABLE IF NOT EXISTS User(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        username TEXT NOT NULL,
        password_hash TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        role TEXT NOT NULL DEFAULT 'user'
    )
    ''')

    conn.execute('''
    CREATE TABLE IF NOT EXISTS Product (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        description TEXT NOT NULL,
        price REAL NOT NULL,
        image_url TEXT UNIQUE NOT NULL,
        is_food BLOB NOT NULL,
        category TEXT NOT NULL,
        stock INTEGER NOT NULL,
        likes INTEGER DEFAULT 0 NOT NULL
    )
    ''')

    conn.execute('''
    CREATE TABLE IF NOT EXISTS UserLikes (
        user_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (user_id, product_id),
        FOREIGN KEY (user_id) REFERENCES User(id) ON DELETE CASCADE,
        FOREIGN KEY (product_id) REFERENCES Product(id) ON DELETE CASCADE
    )
    ''')

    conn.execute('''CREATE TABLE IF NOT EXISTS CartItem (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL DEFAULT 1,
        FOREIGN KEY (user_id) REFERENCES User(id) ON DELETE CASCADE,
        FOREIGN KEY (product_id) REFERENCES Product(id) ON DELETE CASCADE,
        UNIQUE(user_id, product_id)
    )''')

    try:
        conn.execute("ALTER TABLE Product ADD COLUMN views INTEGER DEFAULT 0")
    except Exception:
        pass

    conn.commit()
    conn.close()

class Users:
    @staticmethod
    def find_by_email(email):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM User WHERE email = ?', (email,))
        user = cursor.fetchone()
        conn.close()
        return user

    @staticmethod
    def find_by_id(id):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM User WHERE id = ?', (id,))
        user = cursor.fetchone()
        conn.close()
        return user

    @staticmethod
    def create(email, username, password, role='user'):
        conn = get_db()
        cursor = conn.cursor()
        hashed_password = generate_password_hash(password)
        cursor.execute('''
            INSERT INTO User (email, password_hash, username, role) VALUES (?, ?, ?, ?)
        ''', (email, hashed_password, username, role))
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        return user_id

    @staticmethod
    def verify_password(hashed_password, password):
        return check_password_hash(hashed_password, password)

        # 🔥 ВСТАВЬ СЮДА (после verify_password, внутри class Users):
    
    @staticmethod
    def _hash_keyword(keyword: str) -> str:
        return hashlib.sha256(keyword.lower().strip().encode()).hexdigest()

    @staticmethod
    def set_recovery_keyword(user_id: int, keyword: str) -> bool:
        """Устанавливает хэш секретного слова"""
        if len(keyword.strip()) < 4:
            return False
        try:
            conn = get_db()
            conn.execute(
                'UPDATE User SET recovery_keyword_hash = ? WHERE id = ?',
                (Users._hash_keyword(keyword), user_id)
            )
            conn.commit()
            conn.close()
            return True
        except Exception:
            return False

    @staticmethod
    def verify_recovery_keyword(email: str, keyword: str) -> dict:
        """Проверяет email + секретное слово"""
        conn = get_db()
        user = conn.execute(
            'SELECT id, recovery_keyword_hash FROM User WHERE email = ?',
            (email.lower().strip(),)
        ).fetchone()
        conn.close()
        
        if not user:
            return {'success': False, 'error': 'Пользователь не найден'}
        if not user['recovery_keyword_hash']:
            return {'success': False, 'error': 'Ключевое слово не настроено'}
        if user['recovery_keyword_hash'] != Users._hash_keyword(keyword):
            return {'success': False, 'error': 'Неверное ключевое слово'}
        
        return {'success': True, 'user_id': user['id']}

    @staticmethod
    def update_password(user_id: int, new_password: str) -> bool:
        """Обновляет пароль пользователя"""
        try:
            conn = get_db()
            conn.execute(
                'UPDATE User SET password_hash = ? WHERE id = ?',
                (generate_password_hash(new_password), user_id)
            )
            conn.commit()
            conn.close()
            return True
        except Exception:
            return False


class Products:
    @staticmethod
    def get_best_by_likes(limit=3):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM Product 
            ORDER BY likes DESC 
            LIMIT ?
        ''', (limit,))
        products = cursor.fetchall()
        conn.close()
        return products
    
    @staticmethod
    def get_by_id(product_id):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Product WHERE id = ?', (product_id,))
        product = cursor.fetchone()
        conn.close()
        return product
    
    @staticmethod
    def get_all():
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Product')
        products = cursor.fetchall()
        conn.close()
        return products
    
    @staticmethod
    def add_like(product_id):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE Product SET likes = likes + 1 WHERE id = ?
        ''', (product_id,))
        conn.commit()
        affected = cursor.rowcount
        conn.close()
        return affected > 0
    
    @staticmethod
    def create(name, description, price, image_url, is_food, category, stock, likes=0):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Product (name, description, price, image_url, is_food, category, stock, likes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, description, price, image_url, is_food, category, stock, likes))
        conn.commit()
        product_id = cursor.lastrowid
        conn.close()
        return product_id


class Cart:
    @staticmethod
    def add_item(user_id, product_id, quantity=1):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO CartItem (user_id, product_id, quantity)
            VALUES (?, ?, ?)
            ON CONFLICT(user_id, product_id) DO UPDATE SET quantity = quantity + ?
        ''', (user_id, product_id, quantity, quantity))
        conn.commit()
        conn.close()
        return True

    @staticmethod
    def get_user_cart(user_id):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT ci.id as cart_id, ci.quantity, 
            p.id as product_id, p.name, p.price, p.image_url, p.category
            FROM CartItem ci
            JOIN Product p ON ci.product_id = p.id
            WHERE ci.user_id = ?
        ''', (user_id,))
        items = cursor.fetchall()
        conn.close()
        return items

    @staticmethod
    def update_quantity(user_id, product_id, quantity):
        conn = get_db()
        cursor = conn.cursor()
        if quantity <= 0:
            cursor.execute('DELETE FROM CartItem WHERE user_id = ? AND product_id = ?', (user_id, product_id))
        else:
            cursor.execute('UPDATE CartItem SET quantity = ? WHERE user_id = ? AND product_id = ?', (quantity, user_id, product_id))
        conn.commit()
        conn.close()

    @staticmethod
    def remove_item(user_id, product_id):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM CartItem WHERE user_id = ? AND product_id = ?', (user_id, product_id))
        conn.commit()
        conn.close()

    @staticmethod
    def clear_cart(user_id):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM CartItem WHERE user_id = ?', (user_id,))
        conn.commit()
        conn.close()

def init_orders_db():
    conn = get_db()
    conn.execute('''
    CREATE TABLE IF NOT EXISTS "Order" (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        status TEXT NOT NULL DEFAULT 'pending',
        total REAL NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES User(id) ON DELETE CASCADE
    )
    ''')
    conn.execute('''
    CREATE TABLE IF NOT EXISTS OrderItem (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        product_name TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        price REAL NOT NULL,
        FOREIGN KEY (order_id) REFERENCES "Order"(id) ON DELETE CASCADE
    )
    ''')
    conn.commit()
    conn.close()

class Orders:
    @staticmethod
    def get_user_orders(user_id):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM "Order" WHERE user_id = ? ORDER BY created_at DESC', (user_id,))
        orders = cursor.fetchall()
        
        result = []
        for order in orders:
            cursor.execute('''
                SELECT oi.product_id, oi.product_name, oi.quantity, oi.price, p.image_url 
                FROM OrderItem oi 
                LEFT JOIN Product p ON oi.product_id = p.id 
                WHERE oi.order_id = ?
            ''', (order['id'],))
            items = cursor.fetchall()
            result.append({
                'id': order['id'],
                'created_at': order['created_at'],
                'status': order['status'],
                'total': order['total'],
                'items': [{
                    'id': item['product_id'],
                    'name': item['product_name'],
                    'quantity': item['quantity'],
                    'price': item['price'],
                    'image': item['image_url']
                } for item in items]
            })
        conn.close()
        return result

    @staticmethod
    def create_order(user_id, cart_items):
        conn = get_db()
        cursor = conn.cursor()
        total = 0
        
        for item in cart_items:
            prod_id = item.get('id')
            qty = item.get('quantity', 1)
            cursor.execute('SELECT name, price FROM Product WHERE id = ?', (prod_id,))
            prod = cursor.fetchone()
            if prod:
                total += prod['price'] * qty
        
        if total == 0:
            conn.close()
            return False

        cursor.execute('INSERT INTO "Order" (user_id, total, status) VALUES (?, ?, ?)', (user_id, total, 'pending'))
        order_id = cursor.lastrowid
        for item in cart_items:
            prod_id = item.get('id')
            qty = item.get('quantity', 1)
            cursor.execute('SELECT name, price FROM Product WHERE id = ?', (prod_id,))
            prod = cursor.fetchone()
            if prod:
                cursor.execute('''
                    INSERT INTO OrderItem (order_id, product_id, product_name, quantity, price)
                    VALUES (?, ?, ?, ?, ?)
                ''', (order_id, prod_id, prod['name'], qty, prod['price']))
        
        conn.commit()
        conn.close()
        return True

class Likes:
    @staticmethod
    def toggle(user_id, product_id):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT 1 FROM UserLikes WHERE user_id = ? AND product_id = ?', (user_id, product_id))
        exists = cursor.fetchone()
        
        if exists:
            cursor.execute('DELETE FROM UserLikes WHERE user_id = ? AND product_id = ?', (user_id, product_id))
            cursor.execute('UPDATE Product SET likes = MAX(0, likes - 1) WHERE id = ?', (product_id,))
            is_liked = False
        else:
            cursor.execute('INSERT INTO UserLikes (user_id, product_id) VALUES (?, ?)', (user_id, product_id))
            cursor.execute('UPDATE Product SET likes = likes + 1 WHERE id = ?', (product_id,))
            is_liked = True
            
        conn.commit()
        conn.close()
        return is_liked

    @staticmethod
    def get_status(user_id, product_id):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT 1 FROM UserLikes WHERE user_id = ? AND product_id = ?', (user_id, product_id))
        status = cursor.fetchone() is not None
        conn.close()
        return status


