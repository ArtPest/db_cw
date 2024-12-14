import streamlit as st
import os
import repositories.models as model_repo
import repositories.materials as material_repo
import repositories.diagrams as diagram_repo
import repositories.tags as tags_repo
import repositories.user_models as user_models_repo
import repositories.users as user_repo

def show_profile_page(email):
    # Получаем информацию о пользователе
    user = user_repo.get_user_by_email(email)

    if user is None:
        st.error("Пользователь не найден.")
        return

    st.title(f"Профиль: {email}")
    st.write(f"Роль: {user['role']}")

    if user['role'] == 'admin':
        st.info("Вы являетесь администратором.")

    # Избранные модели пользователя
    st.subheader("Избранные модели")
    favorite_models = user_models_repo.get_favorite_models_by_user_id(user['user_id'])

    if not favorite_models:
        st.write("У вас пока нет избранных моделей.")
    else:
        for model in favorite_models:
            st.write(f"### {model['model_name']}")
            st.write(f"Описание: {model['description']}")
            st.write(f"Сложность: {model['difficulty_level']}")

            # Получаем последнюю диаграмму для отображения на главной странице
            diagrams = diagram_repo.get_diagrams_by_model_id(model['model_id'])
            if diagrams:
                last_diagram = diagrams[-1]  # Последняя диаграмма
                image_path = last_diagram["image_path"]
                if os.path.exists(image_path):
                    st.image(image_path)
                else:
                    st.image("no_image_found.jpg", caption="(изображение отсутствует)")
            else:
                st.image("no_image_found.jpg", caption="Диаграммы отсутствуют")

            # Кнопка для перехода к модели
            if st.button(f"Перейти к {model['model_name']}", key=f"model_button_{model['model_id']}"):
                # Сохраняем ID модели и переходим на страницу модели
                st.session_state.page = "model"
                st.session_state.model_id = model['model_id']
                st.session_state.model_name = model['model_name']  # Сохраняем имя модели для отображения
                st.rerun()  # Перезагружаем страницу

            # Кнопка для удаления из избранного
            if st.button(f"Удалить {model['model_name']} из избранного", key=f"remove_button_{model['model_id']}"):
                user_models_repo.remove_model_from_favorites(user['user_id'], model['model_id'])
                st.rerun()  # Перезагружаем страницу, чтобы обновить интерфейс

            st.write("---")

    # Раздел для удаления учетной записи
    st.subheader("Удаление учетной записи")
    st.write("Чтобы удалить учетную запись, введите свой пароль для подтверждения.")

    password = st.text_input("Введите пароль для удаления", type="password")

    if st.button("Удалить учетную запись"):
        if user_repo.check_password(email, password):
            delete_error = user_repo.delete_user(user['user_id'])
            if delete_error is None:
                st.success("Учетная запись успешно удалена.")
                # Сброс сессии и перезагрузка для возвращения к экрану входа
                st.session_state["authenticated"] = False
                st.session_state["admin"] = False
                st.session_state["user"] = None
                if st.button("Вернуться на главную"):
                    st.session_state.page = "main"
                    st.rerun()
            else:
                st.error(delete_error)  # Показываем ошибку, если не удалось удалить
        else:
            st.error("Неверный пароль. Попробуйте снова.")

    # Логика для страницы модели
    if 'page' in st.session_state and st.session_state.page == "model" and 'model_id' in st.session_state:
        model_id = st.session_state.model_id
        model = model_repo.get_model_by_id(model_id)

        if model is None:
            st.error("Модель не найдена.")
            st.session_state.page = "main"  # Возвращаем на главную страницу
            st.rerun()

        st.title(f"Модель: {model[1]}")
        st.write(f"Описание: {model[2]}")
        st.write(f"Уровень сложности: {model[3]}")

        # Отображаем теги модели
        st.subheader("Теги")
        tags = tags_repo.get_tags_by_model_id(model_id)
        if tags:
            st.write(", ".join(tags))
        else:
            st.write("Нет тегов для этой модели.")

        # Материалы
        st.subheader("Материалы")
        materials = material_repo.get_materials_by_model_id(model_id)
        for material in materials:
            st.write(f"- {material[1]}, {material[2]}, {material[3]}, {material[4]} листов")

        # Диаграммы шагов
        st.subheader("Диаграммы")
        diagrams = diagram_repo.get_diagrams_by_model_id(model_id)

        if diagrams:
            for diagram in diagrams:
                if os.path.exists(diagram['image_path']):
                    st.image(diagram['image_path'], caption=f"Шаг {diagram['diagram_order']}")
                else:
                    st.image("no_image_found.jpg", caption=f"Шаг {diagram['diagram_order']} (изображение отсутствует)")
        else:
            st.image("no_image_found.jpg", caption="Диаграммы отсутствуют")

        # Проверка, находится ли модель в избранном у текущего пользователя
        user_id = st.session_state.user["user_id"]
        is_in_favorites = user_models_repo.is_model_in_favorites(user_id, model_id)

        # Кнопка для возвращения на главную страницу
        if st.button("Вернуться на главную"):
            st.session_state.page = "main"
            st.rerun()  # Перезагружаем страницу

# Запускаем функцию отображения страницы
if __name__ == "__main__":
    email = "user@example.com"  # Здесь будет email текущего пользователя
    show_profile_page(email)
