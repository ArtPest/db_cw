import services.db as db
import pandas as pd

def add_user(email: str, hashed_password: str, role: str = 'user') -> int:
    """Добавление нового пользователя в базу данных"""
    query = """
        INSERT INTO users (email, password, role)
        VALUES (%s, %s, %s)
        RETURNING user_id;
    """
    # Выполнение запроса и возвращение user_id
    result = db.execute_query(query, (email, hashed_password, role))
    return result[0]['user_id']

def get_user_by_email(email: str) -> dict:
    """Получение пользователя по email"""
    query = """
        SELECT * FROM users WHERE email = %s;
    """
    result = db.execute_query(query, (email,))
    if result:
        return result[0]
    return None

def get_user_by_id(user_id: int) -> dict:
    """Получение пользователя по ID"""
    query = """
        SELECT * FROM users WHERE user_id = %s;
    """
    result = db.execute_query(query, (user_id,))
    if result:
        return result[0]
    return None

def get_all_users() -> pd.DataFrame:
    """Получение всех пользователей"""
    query = """
        SELECT * FROM users;
    """
    result = db.execute_query(query)
    return pd.DataFrame(result)
