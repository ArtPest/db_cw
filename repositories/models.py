import psycopg2
from services.db import get_connection  # Подключение к базе данных

def get_all_models():
    """
    Получить все модели оригами.
    Возвращает список моделей с данными (ID, название, описание, уровень сложности).
    """
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT model_id, name, description, difficulty_level FROM models ORDER BY name"
            )
            models = cursor.fetchall()
            return models
    except Exception as e:
        print(f"Ошибка при получении моделей: {e}")
        return []
    finally:
        conn.close()

def get_model_by_id(model_id):
    """
    Получить модель оригами по ID.
    Возвращает информацию о модели (ID, название, описание, уровень сложности, автор).
    """
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT model_id, name, description, difficulty_level FROM models WHERE model_id = %s",
                [model_id]
            )
            model = cursor.fetchone()
            return model if model else None
    except Exception as e:
        print(f"Ошибка при получении модели по ID: {e}")
        return None
    finally:
        conn.close()

def add_model(name, description, difficulty_level):
    """
    Добавить новую модель оригами.
    Возвращает ID добавленной модели.
    """
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO models (name, description, difficulty_level, author_id) "
                "VALUES (%s, %s, %s, %s) RETURNING model_id",
                [name, description, difficulty_level]
            )
            model_id = cursor.fetchone()[0]
            conn.commit()
            return model_id
    except Exception as e:
        print(f"Ошибка при добавлении модели: {e}")
        return None
    finally:
        conn.close()

def update_model(model_id, name, description, difficulty_level):
    """
    Обновить информацию о модели оригами.
    Возвращает True, если обновление успешно, иначе False.
    """
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "UPDATE models SET name = %s, description = %s, difficulty_level = %s WHERE model_id = %s",
                [name, description, difficulty_level, model_id]
            )
            conn.commit()
            return True
    except Exception as e:
        print(f"Ошибка при обновлении модели: {e}")
        return False
    finally:
        conn.close()


def get_models_by_tag_and_difficulty(tag: int, difficulty: str) -> object:
    """
    Получить модели оригами по тегу и уровню сложности.
    Возвращает список моделей с данными (ID, название, описание, уровень сложности).
    """
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            # Строим запрос динамически, чтобы учитывать выбор "Все"
            query = """
                SELECT m.model_id, m.name, m.description, m.difficulty_level
                FROM models m
                JOIN model_tags mt ON m.model_id = mt.model_id
                WHERE 1=1
            """
            params = []

            # Если выбран конкретный тег, добавляем его в запрос
            if tag != -1:
                query += " AND mt.tag_id = %s"
                params.append(tag)

            # Если выбран конкретный уровень сложности, добавляем его в запрос
            if difficulty != "Все":
                query += " AND m.difficulty_level = %s"
                params.append(difficulty)

            # Добавляем GROUP BY после фильтрации
            query += " GROUP BY m.model_id"

            cursor.execute(query, params)
            models = cursor.fetchall()
            return models
    except Exception as e:
        print(f"Ошибка при получении моделей по тегу и сложности: {e}")
        return []
    finally:
        conn.close()

def get_models_by_author(author_id):
    """
    Получить все модели по автору с указанным author_id.
    Возвращает список моделей.
    """
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT model_id, name, description, difficulty_level FROM models WHERE author_id = %s ORDER BY name",
                [author_id]
            )
            models = cursor.fetchall()
            return models
    except Exception as e:
        print(f"Ошибка при получении моделей: {e}")
        return []
    finally:
        conn.close()

def delete_model(model_id):
    """
    Удалить модель оригами по ID.
    Возвращает True, если удаление успешно, иначе False.
    """
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "DELETE FROM models WHERE model_id = %s",
                [model_id]
            )
            conn.commit()
            return True
    except Exception as e:
        print(f"Ошибка при удалении модели: {e}")
        return False
    finally:
        conn.close()
