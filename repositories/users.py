import psycopg2
import bcrypt
from services.db import get_connection  # Подключение к базе данных

def get_user_by_email(email):
    """
    Получает пользователя по email.
    Возвращает данные пользователя или None, если пользователь не найден.
    """
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT user_id, email, password, role FROM users WHERE email = %s", [email]
            )
            user = cursor.fetchone()
            if user:
                return {
                    "user_id": user[0],
                    "email": user[1],
                    "password": user[2],
                    "role": user[3]
                }
            return None
    except Exception as e:
        print(f"Ошибка при получении пользователя по email {email}: {e}")
        return None
    finally:
        conn.close()

def get_user_by_id(user_id):
    """
    Получает пользователя по user_id.
    Возвращает данные пользователя или None, если пользователь не найден.
    """
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT user_id, email, password, role FROM users WHERE user_id = %s", [user_id]
            )
            user = cursor.fetchone()
            if user:
                return {
                    "user_id": user[0],
                    "email": user[1],
                    "password": user[2],
                    "role": user[3]
                }
            return None
    except Exception as e:
        print(f"Ошибка при получении пользователя по user_id {user_id}: {e}")
        return None
    finally:
        conn.close()

def add_user(email, password, role="user"):
    """
    Добавляет нового пользователя в таблицу users.
    Возвращает user_id нового пользователя.
    """
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO users (email, password, role) VALUES (%s, %s, %s) RETURNING user_id",
                [email, password, role]
            )
            user_id = cursor.fetchone()[0]
            conn.commit()
            return user_id
    except Exception as e:
        print(f"Ошибка при добавлении пользователя: {e}")
        return None
    finally:
        conn.close()

def update_user_role(user_id, role):
    """
    Обновляет роль пользователя.
    Принимает user_id и новую роль.
    """
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "UPDATE users SET role = %s WHERE user_id = %s", [role, user_id]
            )
            conn.commit()
            return True
    except Exception as e:
        print(f"Ошибка при обновлении роли пользователя {user_id}: {e}")
        return False
    finally:
        conn.close()

def delete_user(user_id):
    """
    Удаляет пользователя из таблицы users.
    Запрещает удаление, если пользователь является единственным администратором.
    Возвращает строку с ошибкой или None в случае успешного удаления.
    """
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            # Проверяем количество администраторов в базе данных
            cursor.execute("SELECT COUNT(*) FROM users WHERE role = %s", ['admin'])
            admin_count = cursor.fetchone()[0]

            cursor.execute("DELETE FROM users WHERE user_id = %s", [user_id])
            conn.commit()
            return None  # Удаление прошло успешно

    except Exception as e:
        print(f"Ошибка при удалении пользователя {user_id}: {e}")
        return "Ошибка при удалении учетной записи. Попробуйте позже."
    finally:
        conn.close()

def get_all_users():
    """
    Получает всех пользователей.
    Возвращает список пользователей.
    """
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT user_id, email, role FROM users")
            users = cursor.fetchall()
            return [
                {"user_id": user[0], "email": user[1], "role": user[2]}
                for user in users
            ]
    except Exception as e:
        print(f"Ошибка при получении всех пользователей: {e}")
        return []
    finally:
        conn.close()

def check_password(email, password):
    """
    Проверяет пароль пользователя по email.
    Возвращает True, если пароль корректен (сравниваем с хэшированным паролем).
    """
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT password FROM users WHERE email = %s", [email]
            )
            result = cursor.fetchone()
            if result and bcrypt.checkpw(password.encode('utf-8'), result[0].encode('utf-8')):
                return True
            return False
    except Exception as e:
        print(f"Ошибка при проверке пароля пользователя {email}: {e}")
        return False
    finally:
        conn.close()

