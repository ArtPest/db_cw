import psycopg2
from services.db import get_connection  # Подключение к базе данных

def get_all_tags():
    """
    Получает все теги из таблицы tags.
    Возвращает список тегов.
    """
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT tag_id, name FROM tags")
            tags = cursor.fetchall()
            return tags
    except Exception as e:
        print(f"Ошибка при получении тегов: {e}")
        return []
    finally:
        conn.close()

def get_tags_by_model_id(model_id: int):
    """
    Получить все теги для модели по её model_id.
    Возвращает список тегов.
    """
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            query = """
                SELECT t.name
                FROM model_tags mt
                JOIN tags t ON mt.tag_id = t.tag_id
                WHERE mt.model_id = %s
            """
            cursor.execute(query, (model_id,))
            tags = cursor.fetchall()
            # Возвращаем список тегов, извлекая строку из каждого кортежа
            return [tag[0] for tag in tags]
    except Exception as e:
        print(f"Ошибка при получении тегов для модели {model_id}: {e}")
        return []
    finally:
        conn.close()

def add_tag(name):
    """
    Добавляет новый тег в таблицу tags.
    Возвращает tag_id нового тега.
    """
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO tags (name) VALUES (%s) RETURNING tag_id", [name]
            )
            tag_id = cursor.fetchone()[0]
            conn.commit()
            return tag_id
    except Exception as e:
        print(f"Ошибка при добавлении тега: {e}")
        return None
    finally:
        conn.close()

def assign_tags_to_model(model_id, tag_ids):
    """
    Присваивает теги модели.
    Принимает model_id и список tag_ids.
    """
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            for tag_id in tag_ids:
                cursor.execute(
                    "INSERT INTO model_tags (model_id, tag_id) VALUES (%s, %s)",
                    [model_id, tag_id]
                )
            conn.commit()
            return True
    except Exception as e:
        print(f"Ошибка при присваивании тегов модели {model_id}: {e}")
        return False
    finally:
        conn.close()

def remove_tags_from_model(model_id, tag_ids):
    """
    Удаляет теги у модели.
    Принимает model_id и список tag_ids.
    """
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            for tag_id in tag_ids:
                cursor.execute(
                    "DELETE FROM model_tags WHERE model_id = %s AND tag_id = %s",
                    [model_id, tag_id]
                )
            conn.commit()
            return True
    except Exception as e:
        print(f"Ошибка при удалении тегов для модели {model_id}: {e}")
        return False
    finally:
        conn.close()
