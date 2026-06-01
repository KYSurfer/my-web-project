from models import get_db

def make_admin(email):
    conn = get_db()
    user = conn.execute(
        'SELECT id, username, role FROM User WHERE email = ?', 
        (email,)
    ).fetchone()
    
    if not user:
        print(f' Пользователь с email "{email}" не найден')
        conn.close()
        return
    
    print(f' Найдено: {user["username"]} (текущая роль: {user["role"]})')
    
    conn.execute(
        'UPDATE User SET role = ? WHERE email = ?', 
        ('admin', email)
    )
    conn.commit()
    conn.close()
    
    print(f' Пользователь "{email}" теперь администратор!')

if __name__ == '__main__':
    make_admin('tvoj_email@example.com')