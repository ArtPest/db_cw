import psycopg2
from psycopg2 import sql
from services.db import get_connection  # Подключение к базе данных

def get_diagrams_by_model_id(model_id):
    """
    Получить все диаграммы для модели с указанным model_id.
    Возвращает список с данными по диаграммам (ID, model_id, путь к изображению, порядок шагов).
    Если изображений нет, возвращается заглушка.
    """
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                sql.SQL("SELECT diagram_id, model_id, image_path, diagram_order FROM diagrams WHERE model_id = %s ORDER BY diagram_order"),
                [model_id]
            )
            diagrams = cursor.fetchall()
            if not diagrams:
                return [{"diagram_id": None, "model_id": model_id, "image_path": "NO_IMAGE_FOUND", "diagram_order": 1}]
            # Преобразуем кортежи в словари для удобства
            diagram_list = [{"diagram_id": d[0], "model_id": d[1], "image_path": d[2], "diagram_order": d[3]} for d in diagrams]
            return diagram_list
    except Exception as e:
        print(f"Ошибка при получении диаграмм: {e}")
        return []
    finally:
        conn.close()

def get_diagram_by_id(diagram_id):
    """
    Получить диаграмму по ID.
    Возвращает информацию о диаграмме или заглушку, если не найдено.
    """
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                sql.SQL("SELECT diagram_id, model_id, image_path, diagram_order FROM diagrams WHERE diagram_id = %s"),
                [diagram_id]
            )
            diagram = cursor.fetchone()
            if diagram:
                return {"diagram_id": diagram[0], "model_id": diagram[1], "image_path": diagram[2], "diagram_order": diagram[3]}
            # Возвращаем заглушку, если диаграмма не найдена
            return {"diagram_id": None, "model_id": None, "image_path": "NO_IMAGE_FOUND", "diagram_order": 1}
    except Exception as e:
        print(f"Ошибка при получении диаграммы: {e}")
        return {"diagram_id": None, "model_id": None, "image_path": "NO_IMAGE_FOUND", "diagram_order": 1}
    finally:
        conn.close()

def add_diagram(model_id, image_path, diagram_order):
    """
    Добавить новую диаграмму для модели оригами.
    Если изображения нет, можно использовать заглушку.
    """
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                sql.SQL("INSERT INTO diagrams (model_id, image_path, diagram_order) VALUES (%s, %s, %s) RETURNING diagram_id"),
                [model_id, image_path, diagram_order]
            )
            diagram_id = cursor.fetchone()[0]
            conn.commit()
            return diagram_id
    except Exception as e:
        print(f"Ошибка при добавлении диаграммы: {e}")
        return None
    finally:
        conn.close()

def update_diagram(diagram_id, model_id, image_path, diagram_order):
    """
    Обновить диаграмму по ID.
    Если изображение не существует, может использоваться заглушка.
    """
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                sql.SQL("UPDATE diagrams SET model_id = %s, image_path = %s, diagram_order = %s WHERE diagram_id = %s"),
                [model_id, image_path, diagram_order, diagram_id]
            )
            conn.commit()
            return True
    except Exception as e:
        print(f"Ошибка при обновлении диаграммы: {e}")
        return False
    finally:
        conn.close()

def delete_diagram(diagram_id):
    """
    Удалить диаграмму по ID.
    """
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                sql.SQL("DELETE FROM diagrams WHERE diagram_id = %s"),
                [diagram_id]
            )
            conn.commit()
            return True
    except Exception as e:
        print(f"Ошибка при удалении диаграммы: {e}")
        return False
    finally:
        conn.close()
