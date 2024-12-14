import repositories.users as user_repo
import bcrypt

class Registration:
    def __init__(self):
        pass

    def hash_password(self, password: str) -> str:
        """Хеширование пароля с использованием bcrypt"""
        salt = bcrypt.gensalt()  # Генерация соли для bcrypt
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password.decode('utf-8')  # возвращаем строку

    def registr(self, email: str, password: str) -> int:
        """Регистрация нового пользователя"""
        # Хеширование пароля перед сохранением
        hashed_password = self.hash_password(password)

        # Добавление пользователя в базу данных
        user_id = user_repo.add_user(email, hashed_password)
        return user_id

    def check_if_user_exists(self, email: str) -> bool:
        """Проверка, существует ли уже пользователь с таким email"""
        user = user_repo.get_user_by_email(email)
        return user is not None
