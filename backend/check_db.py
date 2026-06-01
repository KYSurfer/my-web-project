import sqlite3

conn = sqlite3.connect('database.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

print("\nПоследние 10 товаров в базе:\n")
cursor.execute('SELECT id, name, price, is_food, category, stock FROM Product ORDER BY id DESC LIMIT 10')
rows = cursor.fetchall()

for row in rows:
    food_label = "ЕДА" if row['is_food'] else "👕 МЕРЧ"
    print(f"{row['id']}. {row['name']} | {row['price']}₽ | {food_label} | {row['category']} | остаток: {row['stock']}")

print(f"\nВсего товаров: {cursor.execute('SELECT COUNT(*) FROM Product').fetchone()[0]}")

conn.close()