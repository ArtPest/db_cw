import repositories.models as model_repo
import repositories.tags as tag_repo
import repositories.materials as material_repo
import pandas as pd

class Catalog:
    def __init__(self):
        pass

    def get_all_models(self) -> pd.DataFrame:
        """Получение всех моделей оригами"""
        return model_repo.get_all_models()

    def get_models_by_tag(self, tag_name: str) -> pd.DataFrame:
        """Получение моделей по тегу"""
        tag = tag_repo.get_tag_by_name(tag_name)
        if tag is None:
            return pd.DataFrame()  # Если тег не найден, возвращаем пустой DataFrame
        return model_repo.get_models_by_tag(tag['tag_id'])

    def get_models_by_difficulty(self, difficulty: str) -> pd.DataFrame:
        """Получение моделей по уровню сложности"""
        return model_repo.get_models_by_difficulty(difficulty)

    def get_models_by_material(self, material_name: str) -> pd.DataFrame:
        """Получение моделей по материалу"""
        material = material_repo.get_material_by_name(material_name)
        if material is None:
            return pd.DataFrame()  # Если материал не найден, возвращаем пустой DataFrame
        return model_repo.get_models_by_material(material['material_id'])

# Пример использования:
# catalog = Catalog()
# all_models = catalog.get_all_models()
# models_by_tag = catalog.get_models_by_tag('животные')
# models_by_difficulty = catalog.get_models_by_difficulty('medium')
