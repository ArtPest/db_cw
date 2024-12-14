import psycopg2
import services.db as db

def is_model_in_favorites(user_id, model_id):
    # Проверяем, добавлена ли модель в избранное
    query = "SELECT * FROM user_models WHERE user_id = %s AND model_id = %s"
    result = db.execute_query(query, (user_id, model_id))
    return len(result) > 0

def add_model_to_favorites(user_id, model_id):
    # Добавляем модель в избранное
    query = "INSERT INTO user_models (user_id, model_id) VALUES (%s, %s)"
    db.execute_query(query, (user_id, model_id))

def remove_model_from_favorites(user_id, model_id):
    # Удаляем модель из избранного
    query = "DELETE FROM user_models WHERE user_id = %s AND model_id = %s"
    db.execute_query(query, (user_id, model_id))

import services.db as db

def get_favorite_models_by_user_id(user_id):
    # Запрос для получения избранных моделей пользователя
    query = """
        SELECT m.model_id, m.name, m.description, m.difficulty_level
        FROM models m   
        JOIN user_models um ON m.model_id = um.model_id
        WHERE um.user_id = %s
    """
    return db.execute_query(query, (user_id,))
