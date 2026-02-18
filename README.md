# SpaceFleet

REST API для управления космическим флотом: корабли, миссии. Проект выполнен на Flask и позволяет управлять флотом с использованием GRUD-оопераций.
___
## Запуск проекта
### 1. Устанавливаем виртуальное окружение
___
#### WINDOWS:
    python -m venv .venv
    source .venv\Scripts\activate
#### LINUX
    virtualenv env
    source env/bin/activate

### 2. Устанавливаем зависимости
    pip install -r requirements.txt

### 3. Запускаем сервер
    python app.py
Сервер будет доступен по адресу http://127.0.0.1:5000
___
## Основные эндпоинты
___
| Метод| URL                             | Описание                      | Пример тела запроса (JSON)                                                                    |
|------|---------------------------------|-------------------------------|-----------------------------------------------------------------------------------------------|
|GET| '/api/v1'                       | Проверка работы сервера       |
|GET| '/api/v1/spaceships'            | Получить список всех кораблей |
|POST| '/api/v1/spaceships'            | Создать новый корабль         | {"spaceship_id": "S001", "name": "Гаусс", "type": "исследовательский", "status": "available"} |
|PUT| '/api/v1/spaceships/<ship_id>'  | Полностью обновить корабль    | {"name": "...", "type": "...", "status": "..."}                                               
|PATH| '/api/v1/spaceships/<ship_id>'  | Частично обновить корабль     | {"status": "в миссии"}                                                                        
|DELETE| '/api/v1/spaceships/<ship_id>'  | Удаление корабля              |
|GET| '/api/v1/missions'              | Получить список всех миссий   |
|POST| '/api/v1/missions'              | Создать новую миссию          | {"mission_id": "M001", "name": "Венера", "qoal": "исследование", "status": "запланирована<br/>"}  |
|PUT| '/api/v1/missions/<mission_id>' | Полностью обновить миссию     | {"mission_id": ...", "name": "...", "qoal": "...", "status": "..."}                           
|PATH| '/api/v1/missions/<mission_id>'    | Частично обновить миссию      | {"status": "в процессе"}                                                                        
|DELETE| '/api/v1/missions/<mission_id>'    | Удаление миссии               | 
|POST|'/api/v1/missions/<mission_id>/spaceships/<ship_id>'| Добавление корабля к миссии|
___
## Примеры запросов curl
#### Проверка работы сервера
curl -X GET http://127.0.0.1:5000/api/v1/spaceships
#### Создание корабля 
curl -X POST http://127.0.0.1:5000/api/v1/spaceships \
  -H "Content-Type: application/json" \
  -d "{\"spaceship_id\": \"S001\", \"name\": \"Гаусс\", \"type\": \"исследовательский\"}"