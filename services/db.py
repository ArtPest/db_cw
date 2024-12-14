import psycopg2
from psycopg2.extras import RealDictCursor
import os

# Получение соединения с базой данных
def get_connection():
    # Подключение к базе данных, замените параметры на свои
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME", "postgres"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "1234"),
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432")
    )

# Выполнение SQL-запроса
def execute_query(query, params=None):
    conn = None
    result = None
    try:
        conn = get_connection()
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, params)
            if query.strip().lower().startswith('select'):
                result = cursor.fetchall()
            else:
                conn.commit()
    except Exception as e:
        print(f"Error executing query: {e}")
    finally:
        if conn:
            conn.close()
    return result
