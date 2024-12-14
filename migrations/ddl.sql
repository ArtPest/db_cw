-- Тип для прав пользователей
CREATE TYPE user_role AS ENUM ('user', 'admin');

-- Таблица пользователей (users)
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    password TEXT NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    role user_role NOT NULL DEFAULT 'user'
);

COMMENT ON TABLE users IS 'Информация о пользователях';
COMMENT ON COLUMN users.user_id IS 'Уникальный идентификатор пользователя';
COMMENT ON COLUMN users.password IS 'Хешированный пароль пользователя';
COMMENT ON COLUMN users.email IS 'Email пользователя';
COMMENT ON COLUMN users.role IS 'Роль пользователя (user или admin)';


-- Таблица моделей оригами (models)
CREATE TABLE models (
    model_id SERIAL PRIMARY KEY,
    model_name VARCHAR(255) NOT NULL,
    description TEXT,
    difficulty_level VARCHAR(50)
);

COMMENT ON TABLE models IS 'Информация о моделях оригами';
COMMENT ON COLUMN models.model_id IS 'Уникальный идентификатор модели';
COMMENT ON COLUMN models.model_name IS 'Название модели';
COMMENT ON COLUMN models.description IS 'Описание модели';
COMMENT ON COLUMN models.difficulty_level IS 'Уровень сложности';

-- Таблица избранного
CREATE TABLE user_models (
    user_id INTEGER REFERENCES users(user_id) ON DELETE CASCADE,
    model_id INTEGER REFERENCES models(model_id) ON DELETE CASCADE,
    PRIMARY KEY (user_id, model_id) -- Композитный ключ для уникальности
);

COMMENT ON TABLE user_models IS 'Связь между пользователем и моделями (модели в избранном)';
COMMENT ON COLUMN user_models.user_id IS 'Идентификатор пользователя';
COMMENT ON COLUMN user_models.model_id IS 'Идентификатор модели';

-- Таблица диаграмм (diagrams)
CREATE TABLE diagrams (
    diagram_id SERIAL PRIMARY KEY,
    model_id INTEGER REFERENCES models(model_id) NOT NULL,
    image_path VARCHAR(255) NOT NULL,
    diagram_order INTEGER NOT NULL
);

COMMENT ON TABLE diagrams IS 'Диаграммы сборки моделей оригами';
COMMENT ON COLUMN diagrams.diagram_id IS 'Уникальный идентификатор диаграммы';
COMMENT ON COLUMN diagrams.model_id IS 'Идентификатор модели';
COMMENT ON COLUMN diagrams.image_path IS 'Путь к изображению диаграммы';
COMMENT ON COLUMN diagrams.diagram_order IS 'Порядковый номер шага';


-- Таблица материалов (materials)
CREATE TABLE materials (
    material_id SERIAL PRIMARY KEY,
    material_name VARCHAR(255) NOT NULL,
    size VARCHAR(50),  -- Например, "15x15 см"
    shape VARCHAR(50)  -- Например, "квадрат", "прямоугольник"
);

COMMENT ON TABLE materials IS 'Список используемых материалов';
COMMENT ON COLUMN materials.material_id IS 'Уникальный идентификатор материала';
COMMENT ON COLUMN materials.material_name IS 'Название материала';
COMMENT ON COLUMN materials.size IS 'Размер материала';
COMMENT ON COLUMN materials.shape IS 'Форма материала';


-- Таблица тегов (tags)
CREATE TABLE tags (
    tag_id SERIAL PRIMARY KEY,
    tag_name VARCHAR(255) UNIQUE NOT NULL
);

COMMENT ON TABLE tags IS 'Теги для моделей';
COMMENT ON COLUMN tags.tag_id IS 'Уникальный идентификатор тега';
COMMENT ON COLUMN tags.tag_name IS 'Название тега';


-- Связующая таблица для моделей и материалов (model_materials)
CREATE TABLE model_materials (
    model_id INTEGER REFERENCES models(model_id) NOT NULL,
    material_id INTEGER REFERENCES materials(material_id) NOT NULL,
    quantity INTEGER NOT NULL,
    PRIMARY KEY (model_id, material_id) --  Композитный ключ для уникальности
);

COMMENT ON TABLE model_materials IS 'Материалы, используемые в модели';
COMMENT ON COLUMN model_materials.model_id IS 'Идентификатор модели';
COMMENT ON COLUMN model_materials.material_id IS 'Идентификатор материала';
COMMENT ON COLUMN model_materials.quantity IS 'Количество';


-- Связующая таблица для моделей и тегов (model_tags)
CREATE TABLE model_tags (
    model_id INTEGER REFERENCES models(model_id) NOT NULL,
    tag_id INTEGER REFERENCES tags(tag_id) NOT NULL,
    PRIMARY KEY (model_id, tag_id) -- Композитный ключ
);

COMMENT ON TABLE model_tags IS 'Связь между моделями и тегами';
COMMENT ON COLUMN model_tags.model_id IS 'Идентификатор модели';
COMMENT ON COLUMN model_tags.tag_id IS 'Идентификатор тега';
