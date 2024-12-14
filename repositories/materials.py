import psycopg2
from psycopg2 import sql
from services.db import get_connection  # Подключение к базе данных

def get_all_materials():
    """
    Получить все материалы.
    Возвращает список материалов с данными (ID, название, размер, форма).
    """
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT material_id, material_name, size, shape FROM materials ORDER BY material_name"
            )
            materials = cursor.fetchall()
            return materials
    except Exception as e:
        print(f"Ошибка при получении материалов: {e}")
        return []
    finally:
        conn.close()

def get_material_by_id(material_id):
    """
    Получить материал по ID.
    Возвращает информацию о материале (ID, название, размер, форма).
    """
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT material_id, material_name, size, shape FROM materials WHERE material_id = %s",
                [material_id]
            )
            material = cursor.fetchone()
            return material if material else None
    except Exception as e:
        print(f"Ошибка при получении материала по ID: {e}")
        return None
    finally:
        conn.close()

def add_material(material_name, size, shape):
    """
    Добавить новый материал в базу данных.
    Возвращает ID добавленного материала.
    """
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO materials (material_name, size, shape) VALUES (%s, %s, %s) RETURNING material_id",
                [material_name, size, shape]
            )
            material_id = cursor.fetchone()[0]
            conn.commit()
            return material_id
    except Exception as e:
        print(f"Ошибка при добавлении материала: {e}")
        return None
    finally:
        conn.close()

def update_material(material_id, material_name, size, shape):
    """
    Обновить информацию о материале.
    Возвращает True, если обновление успешно, иначе False.
    """
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "UPDATE materials SET material_name = %s, size = %s, shape = %s WHERE material_id = %s",
                [material_name, size, shape, material_id]
            )
            conn.commit()
            return True
    except Exception as e:
        print(f"Ошибка при обновлении материала: {e}")
        return False
    finally:
        conn.close()

def get_materials_by_model_id(model_id):
    """
    Получить все материалы, связанные с моделью по model_id.
    Возвращает список материалов (ID, название, размер, форма).
    """
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT m.material_id, m.material_name, m.size, m.shape, mm.quantity
                FROM materials m
                JOIN model_materials mm ON m.material_id = mm.material_id
                WHERE mm.model_id = %s
                """,
                [model_id]
            )
            materials = cursor.fetchall()
            return materials
    except Exception as e:
        print(f"Ошибка при получении материалов для модели {model_id}: {e}")
        return []
    finally:
        conn.close()


def delete_material(material_id):
    """
    Удалить материал по ID.
    Возвращает True, если удаление успешно, иначе False.
    """
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "DELETE FROM materials WHERE material_id = %s",
                [material_id]
            )
            conn.commit()
            return True
    except Exception as e:
        print(f"Ошибка при удалении материала: {e}")
        return False
    finally:
        conn.close()
