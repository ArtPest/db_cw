-- Отключаем временно проверку внешних ключей для успешного удаления всех зависимостей
ALTER TABLE model_tags DROP CONSTRAINT IF EXISTS model_tags_model_id_fkey;
ALTER TABLE model_tags DROP CONSTRAINT IF EXISTS model_tags_tag_id_fkey;
ALTER TABLE model_materials DROP CONSTRAINT IF EXISTS model_materials_model_id_fkey;
ALTER TABLE model_materials DROP CONSTRAINT IF EXISTS model_materials_material_id_fkey;
ALTER TABLE diagrams DROP CONSTRAINT IF EXISTS diagrams_model_id_fkey;
ALTER TABLE user_models DROP CONSTRAINT IF EXISTS user_models_user_id_fkey;
ALTER TABLE user_models DROP CONSTRAINT IF EXISTS user_models_model_id_fkey;

-- Удаляем таблицы в нужном порядке для каскадного удаления
DROP TABLE IF EXISTS model_tags CASCADE;
DROP TABLE IF EXISTS model_materials CASCADE;
DROP TABLE IF EXISTS diagrams CASCADE;
DROP TABLE IF EXISTS user_models CASCADE;
DROP TABLE IF EXISTS models CASCADE;
DROP TABLE IF EXISTS tags CASCADE;
DROP TABLE IF EXISTS materials CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- Если необходимо, удаляем также созданные типы
DROP TYPE IF EXISTS user_role CASCADE;
