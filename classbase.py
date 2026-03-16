
#класс космического коробля
class Spaceship:
    def __init__(self, spaceship_id, name, type_, status="available"):
        self.spaceship_id = spaceship_id
        self.name = name
        self.type_ = type_
        self.status = status
   #обновление статуса
    def update_status(self, new_status):
        self.status = new_status

    # сериализация в словарь для JSON
    def to_dict(self):
        return {
            "spaceship_id": self.spaceship_id,
            "name": self.name,
            "type": self.type_,
            "status": self.status
        }

    #вывод информации
    def __repr__(self):
        return f'Spaceship({self.spaceship_id}, {self.name},{self.type_}, {self.status})'

#миссия
class Mission:
    def __init__(self, mission_id, name, goal, status="planned"):
        self.mission_id = mission_id
        self.name = name
        self.goal = goal
        self.status = status
        self.spaceships = []

    #добавление корабля к миссии
    def add_spaceship(self, spaceship):
        self.spaceships.append(spaceship)

    # сериализация в словарь для JSON
    def to_dict(self):
        return {
            "mission_id": self.mission_id,
            "name": self.name,
            "goal": self.goal,
            "status": self.status,
            # при необходимости можно добавить количество кораблей или их ID
            "ships_count": len(self.spaceships)
        }

    # вывод информации о миссии
    def __repr__(self):
        return (f"Mission(id={self.mission_id}, name={self.name},"
                f" goal={self.goal}, status={self.status}, "
                f"ships={len(self.spaceships)})")

#экипаж
class CrewMember:
    def __init__(self, member_id, name, role):
        self.member_id = member_id
        self.name = name
        self.role = role

    # вывод информации об экипаже
    def __repr__(self):
        return f"CrewMember(id={self.member_id}, name={self.name}, role={self.role})"

