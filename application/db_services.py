from .db import db, User, Monsters

def get_user(uuid=None, ip=None):
    if ip:
        return db.session.query(User).filter_by(ip=ip).first()
    if uuid:
        return db.session.query(User).filter_by(uuid=uuid).one()
    return None

def register_user(uuid, ip):
    if get_user(uuid=uuid, ip=ip):
        return False
    new_user = User(uuid=uuid, ip=ip)
    db.session.add(new_user)
    db.session.commit()
    return True

class MonsterObj:
    def __init__(self, id, name, health, max_health, attack_power, url):
        self.id = id
        self.name = name
        self.health = health
        self.max_health = max_health
        self.attack_power = attack_power
        self.url = url

def get_monster():
    current_monster = db.session.query(Monsters).filter_by(active=True).first()
    return MonsterObj(
        id=current_monster.id,
        name=current_monster.name,
        health=current_monster.health,
        max_health=current_monster.max_health,
        attack_power=current_monster.attack_power,
        url=current_monster.url
    ) if current_monster else None