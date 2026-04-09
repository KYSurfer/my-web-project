import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config

def get_db():
    connection = sqlite3.connect(Config.DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection

def init_db():
    conn = get_db()
    conn.execute('''
    CREATE TABLE IF NOT EXISTS User(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        username TEXT NOT NULL,
        password_hash TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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

    conn.execute('''CREATE TABLE IF NOT EXISTS CartItem (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL DEFAULT 1,
        FOREIGN KEY (user_id) REFERENCES User(id) ON DELETE CASCADE,
        FOREIGN KEY (product_id) REFERENCES Product(id) ON DELETE CASCADE,
        UNIQUE(user_id, product_id)
    )''')

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
    def create(email, username, password):
        conn = get_db()
        cursor = conn.cursor()
        hashed_password = generate_password_hash(password)
        cursor.execute('''
            INSERT INTO User (email, password_hash, username) VALUES (?, ?, ?)
        ''', (email, hashed_password, username))
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        return user_id

    @staticmethod
    def verify_password(hashed_password, password):
        return check_password_hash(hashed_password, password)


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