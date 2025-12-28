import psycopg2
from psycopg2 import Error

print("=== ПОДКЛЮЧЕНИЕ К POSTGRESQL ИЗ PYTHON ===\n")

try:
    # 1. ПОДКЛЮЧАЕМСЯ К БАЗЕ ДАННЫХ
    print("1. Подключаемся к базе данных 'my_learning_db'...")

    connection = psycopg2.connect(
        dbname="my_learning_db",  # имя базы, которую мы создали
        user="postgres",  # пользователь
        password="postgres",  # пароль от PostgreSQL
        host="localhost",  # сервер
        port="5432"  # порт
    )

    print("✅ Успешно подключились к PostgreSQL!")

    # 2. СОЗДАЕМ КУРСОР ДЛЯ ВЫПОЛНЕНИЯ ЗАПРОСОВ
    cursor = connection.cursor()

    # 3. ВЫПОЛНЯЕМ ПРОСТОЙ ЗАПРОС
    print("\n2. Выполняем тестовый запрос...")
    cursor.execute("SELECT version();")
    db_version = cursor.fetchone()
    print(f"   Версия PostgreSQL: {db_version[0]}")

    # 4. ПОЛУЧАЕМ ДАННЫЕ ИЗ НАШЕЙ ТАБЛИЦЫ users
    print("\n3. Получаем данные из таблицы 'users':")
    cursor.execute("SELECT id, name, email, age FROM users ORDER BY id;")

    users = cursor.fetchall()
    print("   ID | Имя            | Email                 | Возраст")
    print("   ---+----------------+-----------------------+--------")

    for user in users:
        print(f"   {user[0]:2d} | {user[1]:14s} | {user[2]:20s} | {user[3]:3d}")

    # 5. СЧИТАЕМ КОЛИЧЕСТВО ПОЛЬЗОВАТЕЛЕЙ
    cursor.execute("SELECT COUNT(*) FROM users;")
    count = cursor.fetchone()[0]
    print(f"\n   Всего пользователей в базе: {count}")

    # 6. ДОБАВЛЯЕМ НОВОГО ПОЛЬЗОВАТЕЛЯ ИЗ PYTHON
    print("\n4. Добавляем нового пользователя из Python...")

    new_user = ('Сергей', 'sergey@example.com', 35)
    cursor.execute(
        "INSERT INTO users (name, email, age) VALUES (%s, %s, %s)",
        new_user
    )
    connection.commit()  # СОХРАНЯЕМ ИЗМЕНЕНИЯ!

    print(f"   ✅ Добавлен: {new_user[0]}, email: {new_user[1]}, возраст: {new_user[2]}")

    # 7. ПРОВЕРЯЕМ, ЧТО ДОБАВИЛОСЬ
    cursor.execute("SELECT COUNT(*) FROM users;")
    new_count = cursor.fetchone()[0]
    print(f"   Теперь пользователей: {new_count}")

except Error as e:
    print(f"❌ Ошибка: {e}")

finally:
    # 8. ЗАКРЫВАЕМ СОЕДИНЕНИЕ
    if connection:
        cursor.close()
        connection.close()
        print("\n✅ Соединение с базой данных закрыто")

print("\n=== Готово! ===")