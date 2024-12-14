-- Заполнение таблицы users
INSERT INTO users (password, email, role) VALUES
('admin', 'admin@example.ru', 'admin');

-- Заполнение таблицы tags (добавлено больше тегов)
INSERT INTO tags (name) VALUES
('животные'),
('птицы'),
('цветы'),
('абстракция'),
('геометрия'),
('деревья'),
('дома'),
('машины'),
('мосты'),
('корабли'),
('самолеты'),
('звери'),
('насекомые'),
('рыбы'),
('кошки'),
('собаки');

-- Заполнение таблицы materials (добавлено больше материалов)
INSERT INTO materials (name, size, shape) VALUES
('бумага', '15x15 см', 'квадрат'),
('бумага', '20x20 см', 'квадрат'),
('цветная бумага', '10x10 см', 'квадрат'),
('картон', '15x15 см', 'квадрат'),
('ткань', '30x40 см', 'прямоугольник'),
('лента', '50 см', 'полоска');

-- Заполнение таблицы models (добавлено больше моделей)
INSERT INTO models (name, description, difficulty_level) VALUES
('Журавлик', 'Классическая модель оригами', 'easy'),
('Лягушка', 'Прыгающая лягушка', 'medium'),
('Лилия', 'Красивый цветок', 'hard'),
('Лодка', 'Небольшая лодка', 'easy'),
('Собака', 'Милая собачка', 'medium'),
('Дом', 'Простой домик', 'easy'),
('Цветок', 'Красивый цветок', 'medium'),
('Жираф', 'Высокий жираф', 'hard'),
('Кусудама', 'Шар из модулей', 'hard');

-- Заполнение таблицы user_models (указание моделей в избранном)
INSERT INTO user_models (user_id, model_id) VALUES
(1, 1),  -- Пользователь 1 добавил модель 1 в избранное
(1, 2);  -- Пользователь 1 добавил модель 2 в избранное

-- Заполнение таблицы diagrams (добавлено больше диаграмм)
INSERT INTO diagrams (model_id, image_path, diagram_order) VALUES
(1, 'images/crane/1.jpg', 1),
(1, 'images/crane/2.jpg', 2),
(2, 'images/frog/1.jpg', 1),
(2, 'images/frog/2.jpg', 2),
(3, 'images/lily/1.jpg', 1),
(3, 'images/lily/2.jpg', 2),
(4, 'images/boat/1.jpg', 1),
(4, 'images/boat/2.jpg', 2),
(5, 'images/dog/1.jpg', 1),
(5, 'images/dog/2.jpg', 2),
(6, 'images/house/1.jpg', 1),
(6, 'images/house/2.jpg', 2),
(7, 'images/flower/1.jpg', 1),
(7, 'images/flower/2.jpg', 2),
(8, 'images/giraffe/1.jpg', 1),
(8, 'images/giraffe/2.jpg', 2),
(9, 'images/kusudama/1.jpg', 1),
(9, 'images/kusudama/2.jpg', 2);

-- Заполнение таблицы model_materials (добавлено больше связей)
INSERT INTO model_materials (model_id, material_id, quantity) VALUES
(1, 1, 1),
(2, 2, 1),
(3, 3, 2),
(4, 1, 1),
(5, 4, 2),
(6, 5, 1),
(7, 3, 1),
(8, 6, 1),
(9, 1, 60),
(9, 4, 30);

-- Заполнение таблицы model_tags (добавлено больше связей)
INSERT INTO model_tags (model_id, tag_id) VALUES
(1, 1),
(1, 2),
(2, 1),
(3, 3),
(4, 10),
(5, 8),
(6, 6),
(7, 3),
(8, 1),
(9, 3);
