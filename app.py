from flask  import Flask
from flask import jsonify
from flask import request

from classbase import Spaceship

app = Flask(__name__)

#@app.route('/api/v1', methods=['GET'])
#def home():
#    return "Сервер работает", 200

#эндпоинты для кораблей
## #хранилище данныx для короблей
spaceships = []

##вспомогательные функции
### поиск кораблей про id
def find_spaceship(ship_id):
    return next((s for s in spaceships if s.spaceship_id == ship_id), None)

##эндпоинты

###возвращает список всех кораблей
@app.route('/api/v1/spaceships', methods = ['GET'])
def get_spaceships():
    return jsonify([s.to_dict()for s in spaceships]), 200

###добавляет новый корабль
app.route('/api/v1/spaceships', methods=['POST'])
def create_spaceship():
    data = request.get_json()
    required = ['spaceship_id', 'name', 'type']
    if not all(k in data for k in required):
        return jsonify({"ошибка": "Отсутствуют оязательные поля"}), 400

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
    return jsonify({"собщение": "Данные о корабле удалены"}), 200



if __name__ == '__main__':
    app.run(debug=True)

