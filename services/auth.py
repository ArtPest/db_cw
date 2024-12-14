import bcrypt
import repositories.users as user_repo


class Auth:
    def __init__(self):
        # Это можно настроить, если нужно подключить дополнительные параметры
        pass

    def auth(self, email: str, password: str) -> bool:
        """Авторизация пользователя по email и паролю"""
        user = user_repo.get_user_by_email(email)
        if user is None:
            return False  # Пользователь не найден

        # Сравнение пароля с хешированным в базе данных
        return bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8'))

    def hash_password(self, password: str) -> str:
        """Хеширование пароля перед сохранением в базу"""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# Пример использования:
# auth = Auth()
# auth.auth('user@example.com', 'user_password')
