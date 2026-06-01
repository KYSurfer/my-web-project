# backend/scripts/migrate_recovery.py
from models import get_db

def migrate_recovery():
    conn = get_db()
    
    try:
        # 🔥 1. Удаляем старую таблицу (если есть)
        conn.execute('DROP TABLE IF EXISTS PasswordRecoveryKeywords')
        print('🗑️ Удалена таблица PasswordRecoveryKeywords')
        
        # 🔥 2. Пробуем добавить колонку в User
        # SQLite не поддерживает "ADD COLUMN IF NOT EXISTS" в старых версиях,
        # поэтому ловим ошибку, если колонка уже есть
        try:
            conn.execute('ALTER TABLE User ADD COLUMN recovery_keyword_hash TEXT')
            print('✅ Добавлена колонка recovery_keyword_hash в User')
        except Exception as e:
            if 'duplicate column name' in str(e).lower():
                print('⚠️ Колонка recovery_keyword_hash уже существует')
            else:
                raise
        
        conn.commit()
        print('🎉 Миграция завершена успешно!')
        
    except Exception as e:
        conn.rollback()
        print(f'❌ Ошибка миграции: {e}')
        raise
    finally:
        conn.close()

if __name__ == '__main__':
    migrate_recovery()