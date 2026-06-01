from models import get_db
from werkzeug.security import generate_password_hash 

def create_admin(username, email, password, role='admin'):
    """Создаёт нового пользователя с ролью администратора"""
    conn = get_db()
    
    existing = conn.execute(
        'SELECT id FROM User WHERE email = ?', 
        (email,)
    ).fetchone()
    
    if existing:
        print(f' Пользователь с email "{email}" уже существует!')
        conn.close()
        return None
    
    password_hash = generate_password_hash(password)
    
    try:
        cursor = conn.execute(
            '''INSERT INTO User (username, email, password_hash, role) 
               VALUES (?, ?, ?, ?)''',
            (username, email, password_hash, role)
        )
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        
        print(f' Админ создан!')
        print(f'   ID: {user_id}')
        print(f'   Логин: {email}')
        print(f'   Пароль: {password}')
        print(f'   Роль: {role}')
        print(f'\n Теперь можно войти на /auth/login')
        return user_id
        
    except Exception as e:
        conn.close()
        print(f' Ошибка при создании: {e}')
        return None

if __name__ == '__main__':
    create_admin(
        username='SuperAdmin',
        email='admins@bonsburgers.local',  
        password='SecurePass123!'          
    )