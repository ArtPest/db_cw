import streamlit as st
import repositories.users as user_repo
import repositories.admin as admin_repo

def show_admin_panel():
    st.title("Панель администратора")

    section = st.sidebar.radio("Выберите раздел", ["Управление пользователями"])

    if section == "Управление пользователями":
        st.header("Управление пользователями")

        users = user_repo.get_all_users()

        # Отображаем таблицу пользователей
        st.write("Список пользователей:")
        st.write(users)

        # Повышение пользователя до администратора
        st.subheader("Повысить пользователя до администратора")
        email = st.text_input("Введите почту пользователя для повышения")

        if st.button("Повысить до администратора"):
            user = user_repo.get_user_by_email(email)
            if user:
                if user['role'] == 'admin':
                    st.error(f"Пользователь {email} уже является администратором.")
                else:
                    admin_repo.set_admin(user['user_id'], True)
                    st.success(f"Пользователь {email} успешно повышен до администратора!")
            else:
                st.error(f"Пользователь с почтой {email} не найден.")

        # Удаление пользователя
        st.subheader("Удалить пользователя")
        delete_email = st.text_input("Введите почту пользователя для удаления")

        if st.button("Удалить пользователя"):
            user = user_repo.get_user_by_email(delete_email)
            if user:
                if user['role'] == 'admin':
                    st.error("Нельзя удалить администратора.")
                else:
                    user_repo.delete_user(user['user_id'])
                    st.success(f"Пользователь {delete_email} успешно удалён!")
            else:
                st.error(f"Пользователь с почтой {delete_email} не найден.")
