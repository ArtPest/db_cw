import psycopg2
from psycopg2 import sql
from services.db import get_connection

def set_admin(user_id, is_admin):
    """
    Изменение роли пользователя на 'admin' или 'user'.
    """
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            new_role = 'admin' if is_admin else 'user'
            cursor.execute(
                sql.SQL("UPDATE users SET role = %s WHERE user_id = %s"),
                [new_role, user_id]
            )
            conn.commit()
            return True
    except Exception as e:
        print(f"Ошибка при изменении роли пользователя: {e}")
        return False
    finally:
        conn.close()

def delete_user(user_id):
    """
    Удаление пользователя из базы данных.
    """
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql.SQL("DELETE FROM users WHERE user_id = %s"), [user_id])
            conn.commit()
            return True
    except Exception as e:
        print(f"Ошибка при удалении пользователя: {e}")
        return False
    finally:
        conn.close()

def get_admin_by_user_id(user_id):
    """
    Проверка, является ли пользователь администратором.
    Возвращает True, если пользователь — администратор, иначе — False.
    """
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                sql.SQL("SELECT role FROM users WHERE user_id = %s"),
                [user_id]
            )
            result = cursor.fetchone()
            if result and result[0] == 'admin':
                return True
            return False
    except Exception as e:
        print(f"Ошибка при проверке роли администратора: {e}")
        return False
    finally:
        conn.close()
