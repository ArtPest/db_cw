import time
import streamlit
import pandas as pd

from repositories.users import get_all_users
from pages.admin_panel import show_admin_panel
from pages.main_page import show_main_page
from pages.profile import show_profile_page
from services.auth import Auth
import services.users
import services.regist
import repositories.admin

users = services.users.get_all_users()
registr = services.regist.Registration()

auth = Auth()  # Создаём объект класса Auth

def login():
    streamlit.title("Авторизация")
    streamlit.write("Введите почту и пароль:")

    email = streamlit.text_input("Почта")
    password = streamlit.text_input("Пароль", type="password")

    if streamlit.button("Войти"):
        if auth.auth(email, password):
            streamlit.session_state["authenticated"] = True
            streamlit.session_state["username"] = email
            streamlit.success(f"Добро пожаловать, {email}!")

            # Получение информации о пользователе
            streamlit.session_state.user = services.users.get_user_by_email(email)

            # Проверка на администратора
            streamlit.session_state["admin"] = repositories.admin.get_admin_by_user_id(
                streamlit.session_state.user["user_id"]
            )

            time.sleep(2.0)
            streamlit.rerun()  # Перезагрузка страницы для отображения интерфейса
        else:
            streamlit.error("Неверная почта или пароль!")


def register():
    streamlit.title("Регистрация")
    email = streamlit.text_input("Почта")
    password = streamlit.text_input("Пароль", type="password")
    second_password = streamlit.text_input("Подтверждение пароля", type="password")

    if streamlit.button("Зарегистрироваться"):
        users = get_all_users()

        # Проверяем, существует ли пользователь с таким email
        if any(user['email'] == email for user in users):
            streamlit.error("Пользователь с таким email уже существует.")
        elif not email or not password or not second_password:
            streamlit.error("Введите требуемые значения!")
        elif password != second_password:
            streamlit.error("Пароли не совпадают!")
        else:
            user_id = registr.registr(email, password)
            user = pd.DataFrame({"user_id": [user_id], "email": [email], "password": [password]})
            streamlit.success("Регистрация прошла успешно! Пожалуйста, войдите в аккаунт.")

            # После успешной регистрации сбрасываем авторизацию
            streamlit.session_state["authenticated"] = False
            streamlit.session_state["admin"] = False
            streamlit.session_state.user = pd.DataFrame(columns=["user_id", "email"])

            time.sleep(2)  # Небольшая задержка для отображения сообщения
            streamlit.rerun()  # Перезагружаем страницу, чтобы показать экран входа

def logout():
    streamlit.session_state["authenticated"] = False
    streamlit.session_state["admin"] = False
    streamlit.session_state.user = pd.DataFrame(columns=["user_id", "email"])
    streamlit.success("Вы вышли из аккаунта.")
    streamlit.rerun()  # Перезагружаем страницу для возврата на экран входа

def main():
    if not streamlit.session_state["authenticated"]:
        pg = streamlit.radio("Войдите или зарегистрируйтесь", ["Вход", "Регистрация"])
        if pg == "Вход":
            login()
        elif pg == "Регистрация":
            register()

    else:
        email = streamlit.session_state.user["email"]

        # Добавляем кнопку выхода
        if streamlit.sidebar.button("Выйти"):
            logout()

        if streamlit.session_state["admin"]:
            page = streamlit.sidebar.radio(
                "Навигация",
                ["Основная", "Профиль", "Панель Администратора"],
            )
            if page == "Профиль":
                show_profile_page(email)
            elif page == "Основная":
                show_main_page()
            elif page == "Панель Администратора":
                show_admin_panel()
        else:
            page = streamlit.sidebar.radio(
                "Навигация",
                ["Основная", "Профиль"],
            )
            if page == "Профиль":
                show_profile_page(email)
            elif page == "Основная":
                show_main_page()

# Инициализация состояния сессии
if "authenticated" not in streamlit.session_state:
    streamlit.session_state["authenticated"] = False

if "admin" not in streamlit.session_state:
    streamlit.session_state["admin"] = False

if "user" not in streamlit.session_state:
    streamlit.session_state.user = pd.DataFrame(columns=["user_id", "email"])

if __name__ == "__main__":
    main()
