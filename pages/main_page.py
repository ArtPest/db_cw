import streamlit as st
import os  # Для проверки существования файла
import repositories.models as model_repo
import repositories.materials as material_repo
import repositories.diagrams as diagram_repo
import repositories.tags as tags_repo
import repositories.user_models as user_models_repo

def show_main_page():
    # Проверяем, на какой странице находится пользователь
    if 'page' not in st.session_state:
        st.session_state.page = "main"  # Главная страница по умолчанию

    # Логика для главной страницы
    if st.session_state.page == "main":
        st.title("Каталог оригами")

        # Получаем все теги, но отображаем только их имена в селекторе
        tags = ["Все"] + [tag[1] for tag in tags_repo.get_all_tags()]

        # Сохраняем mapping для быстрого доступа к tag_id
        tag_map = {tag[1]: int(tag[0]) for tag in tags_repo.get_all_tags()}
        tag_map["Все"] = -1  # Для тега "Все" оставляем значение как "Все"

        # Отображаем селектор с именами тегов
        selected_tag_name = st.sidebar.selectbox("Выберите тег", options=tags, index=0)

        # Получаем соответствующий tag_id
        selected_tag_id = tag_map.get(selected_tag_name, None)

        # Уровень сложности
        difficulty = st.sidebar.selectbox("Выберите уровень сложности", options=["Все", "easy", "medium", "hard"],
                                          index=0)

        # Получаем модели по выбранному тегу и сложности
        models = model_repo.get_models_by_tag_and_difficulty(selected_tag_id, difficulty)

        st.subheader("Модели оригами")

        if not models:
            st.write("Нет моделей, соответствующих выбранным критериям.")

        for model in models:
            st.write(f"### {model[1]}")
            st.write(f"Описание: {model[2]}")
            st.write(f"Уровень сложности: {model[3]}")

            # Получаем последнюю диаграмму для отображения на главной странице
            diagrams = diagram_repo.get_diagrams_by_model_id(model[0])
            if diagrams:
                last_diagram = diagrams[-1]  # Последняя диаграмма
                image_path = last_diagram["image_path"]
                if os.path.exists(image_path):
                    st.image(image_path)
                else:
                    st.image("no_image_found.jpg")
            else:
                st.image("no_image_found.jpg")

            # Кнопка для перехода к модели
            if st.button(f"Перейти к {model[1]}", key=f"model_button_{model[0]}"):
                # Сохраняем ID модели и переходим на страницу модели
                st.session_state.page = "model"
                st.session_state.model_id = model[0]
                st.rerun()  # Перезагружаем страницу

            st.write("---")

    # Логика для страницы модели
    elif st.session_state.page == "model" and 'model_id' in st.session_state:
        model_id = st.session_state.model_id
        model = model_repo.get_model_by_id(model_id)

        if model is None:
            st.error("Модель не найдена.")
            return

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

        # Кнопка для добавления/удаления модели из избранного
        if is_in_favorites:
            if st.button("Удалить из избранного"):
                user_models_repo.remove_model_from_favorites(user_id, model_id)
                st.rerun()
        else:
            if st.button("Добавить в избранное"):
                user_models_repo.add_model_to_favorites(user_id, model_id)
                st.rerun()  # Перезагружаем страницу, чтобы обновить интерфейс

        # Кнопка для возвращения на главную страницу
        if st.button("Вернуться на главную"):
            st.session_state.page = "main"
            st.rerun()  # Перезагружаем страницу

# Запускаем функцию отображения страницы
if __name__ == "__main__":
    show_main_page()
