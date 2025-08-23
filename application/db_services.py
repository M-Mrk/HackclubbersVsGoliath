from .db import db, User, Monsters, Attacks
from uuid import uuid4

def get_user(uuid=None, ip=None):
    if ip:
        return db.session.query(User).filter_by(ip=ip).first()
    if uuid:
        return db.session.query(User).filter_by(uuid=uuid).one()
    return None

def register_user(uuid, ip):
    new_user = User(uuid=uuid, ip=ip)
    db.session.add(new_user)
    db.session.commit()

def get_uuid(uuid=None, ip=None):
    if not uuid and not ip:
        raise ValueError("Either uuid or ip must be provided")
    user = get_user(uuid=uuid, ip=ip)
    if not user:
        uuid = str(uuid4())
        register_user(uuid=uuid, ip=ip)
        user = get_user(uuid=uuid, ip=ip)
    return user.uuid if user else None

class MonsterObj:
    def __init__(self, id, name, health, max_health, attack_power, url):
        self.id = id
        self.name = name
        self.health = health
        self.max_health = max_health
        self.attack_power = attack_power
        self.url = url

def get_monster():
    try:
        current_monster = db.session.query(Monsters).filter_by(active=True).one()
        return MonsterObj(
            id=current_monster.id,
            name=current_monster.name,
            health=current_monster.health,
            max_health=current_monster.max_health,
            attack_power=current_monster.attack_power,
            url=current_monster.url
        ) if current_monster else None
    except Exception as e:
        print(f"Error fetching monster: {e}")
        return None

def get_last_attacks():
    return db.session.query(Attacks).order_by(Attacks.created_at.desc()).limit(10).all()