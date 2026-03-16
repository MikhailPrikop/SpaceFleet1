from flask  import Flask
from flask import jsonify
from flask import request

from classbase import Spaceship, Mission

app = Flask(__name__)

@app.route('/api/v1', methods=['GET'])
def home():
    return "Сервер работает", 200

#эндпоинты для кораблей
## хранилище данныx для короблей, миссии
spaceships = []
missions = []



##вспомогательные функции
### поиск кораблей про id
def find_spaceship(ship_id):
    return next((s for s in spaceships if s.spaceship_id == ship_id), None)

### поиск миссии
def find_mission(mission_id):
    return next((m for m in missions if m.mission_id == mission_id), None)

##эндпоинты

###возвращает список всех кораблей
@app.route('/api/v1/spaceships', methods = ['GET'])
def get_spaceships():
    return jsonify([s.to_dict()for s in spaceships]), 200

###добавляет новый корабль
@app.route('/api/v1/spaceships', methods=['POST'])
def create_spaceship():
    data = request.get_json()
    required = ['spaceship_id', 'name', 'type']
    if not all(k in data for k in required):
        return jsonify({"ошибка": "Отсутствуют обязательные поля"}), 400

    #### проверка уеникальности корабляя
    if find_spaceship(data['spaceship_id']):
        return jsonify({"ошибка": "Космический корабль с таким ID уже существует"}), 400

    ship = Spaceship(
        spaceship_id=data['spaceship_id'],
        name=data['name'],
        type_=data['type'],
        status=data.get('status', 'available')
    )
    spaceships.append(ship)
    return jsonify(ship.to_dict()), 201

###обновление данныx корабля

#### полное обновление
@app.route('/api/v1/spaceships/<ship_id>', methods=['PUT'])
def update_spaceship(ship_id):
    ship = find_spaceship(ship_id)
    if not ship:
        return jsonify({"ошибка": "Корабль не найден"}), 404

    data = request.get_json()
    required = ['name', 'type', 'status']
    if not all(k in data for k in required):
        return jsonify({"ошибка": "Отсутствуют обязательные поля"}), 400

    ship.name = data['name']
    ship.type_ = data['type']
    ship.status = data['status']
    return jsonify(ship.to_dict()), 200

#### частичное обновление
@app.route('/api/v1/spaceships/<ship_id>', methods=['PATCH'])
def patch_spaceship(ship_id):
    ship = find_spaceship(ship_id)
    if not ship:
        return jsonify({"ошибка": "Корабль не найден"}), 404

    data = request.get_json()
    if 'name' in data:
        ship.name = data['name']
    if 'type' in data:
        ship.type_ = data['type']
    if 'status' in data:
        ship.status = data['status']
    return jsonify(ship.to_dict()), 200

### удаление корабля
@app.route('/api/v1/spaceships/<ship_id>', methods=['DELETE'])
def delete_spaceship(ship_id):
    ship = find_spaceship(ship_id)
    if not ship:
        return jsonify({"ошибка": "Корабль не найден"}), 404

    for mission in missions:
        if ship in mission.spaceships:
            mission.spaceships.remove(ship)

    spaceships.remove(ship)
    return jsonify({"сообщение": "Данные о корабле удалены"}), 200

#============================ МИССИИ ============================
###возвращает список всех миссий
@app.route('/api/v1/missions', methods = ['GET'])
def get_missionas():
    return jsonify([s.to_dict()for s in missions]), 200

###добавляет новую миссию
@app.route('/api/v1/missions', methods=['POST'])
def create_mission():
    data = request.get_json()
    required = ['mission_id', 'name', 'goal']
    if not all(k in data for k in required):
        return jsonify({"ошибка": "Отсутствуют обязательные поля"}), 400

    #### проверка уеникальности корабляя
    if find_mission(data['mission_id']):
        return jsonify({"ошибка": "Миссия с таким ID уже существует"}), 400

    mission = Mission(
        mission_id=data['mission_id'],
        name=data['name'],
        goal=data['goal'],
        status=data.get('status', 'planned')
    )
    missions.append(mission)
    return jsonify(mission.to_dict()), 201

###обновление данныx
@app.route('/api/v1/missions/<mission_id>', methods=['PUT'])
def update_mission(mission_id):
    mission = find_mission(mission_id)
    if not mission:
        return jsonify({"ошибка": "Миссия не найдена"}), 404

    data = request.get_json()
    required = ['name', 'goal', 'status']
    if not all(k in data for k in required):
        return jsonify({"ошибка": "Отсутствуют обязательные поля"}), 400

    mission.name = data['name']
    mission.goal = data['goal']
    mission.status = data['status']
    return jsonify(mission.to_dict()), 200

@app.route('/api/v1/missions/<mission_id>', methods=['PATCH'])
def patch_mission(mission_id):
    mission = find_mission(mission_id)
    if not mission:
        return jsonify({"ошибка": "Миссия не найдена"}), 404

    data = request.get_json()
    if 'name' in data:
        mission.name = data['name']
    if 'goal' in data:
        mission.goal = data['goal']
    if 'status' in data:
        mission.status = data['status']
    return jsonify(mission.to_dict()), 200

###удаление миссии
@app.route('/api/v1/missions/<mission_id>', methods=['DELETE'])
def delete_mission(mission_id):
    mission = find_mission(mission_id)
    if not mission:
        return jsonify({"ошибка": "Миссия не найдена"}), 404

    missions.remove(mission)
    return jsonify({"сообщение": "Миссия удалена"}), 200

###добваление корабля к миссии
@app.route('/api/v1/missions/<mission_id>/spaceships/<ship_id>', methods=['POST'])
def add_spaceship_to_mission(mission_id, ship_id):
    mission = find_mission(mission_id)
    if not mission:
        return jsonify({"ошибка": "Миссия не найдена"}), 404

    ship = find_spaceship(ship_id)
    if not ship:
        return jsonify({"ошибка": "Корабль не найден"}), 404

    if ship in mission.spaceships:
        return jsonify({"ошибка": "Данный корабль уже включен в заданную миссию"}), 400

    mission.add_spaceship(ship)
    ship.update_status("в миссии")
    return jsonify({"сообщение": "Корабль добавлен в миссию"}), 200

if __name__ == '__main__':
    app.run(debug=True)

