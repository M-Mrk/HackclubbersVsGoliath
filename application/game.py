from .db import db, User, Monsters, Attacks
from datetime import datetime, timezone, timedelta

COOLDOWN = timedelta(hours=23) # 23 instead of 24 to avoid endless shifting
STRONG_MONSTER_DAMAGE = 10
WEAK_MONSTER_DAMAGE = 1

def get_attack_status(user_uuid):
    user = db.session.query(User).filter_by(uuid=user_uuid).one()
    if user.attacked_at:
        current_time = datetime.now(timezone.utc)
        if current_time - user.attacked_at.replace(tzinfo=timezone.utc) > COOLDOWN:
            return True
        else:
            time_left = COOLDOWN - (current_time - user.attacked_at.replace(tzinfo=timezone.utc))
            return time_left
    return True

def attack_strong_monster(user_uuid):
    user = db.session.query(User).filter_by(uuid=user_uuid).one()
    if get_attack_status(user_uuid) == True:
        monster = db.session.query(Monsters).filter_by(active=True).one()
        attack = Attacks(user_id=user.id, monster_id=monster.id, damage=STRONG_MONSTER_DAMAGE, attack_type="strong")
        db.session.add(attack)
        monster.health -= STRONG_MONSTER_DAMAGE
        user.attacked_at = datetime.now(timezone.utc)
        db.session.commit()
        return True
    return False

def attack_weak_monster(user_uuid):
    user = db.session.query(User).filter_by(uuid=user_uuid).one()
    monster = db.session.query(Monsters).filter_by(active=True).one()
    attack = Attacks(user_id=user.id, monster_id=monster.id, damage=WEAK_MONSTER_DAMAGE, attack_type="weak")
    db.session.add(attack)
    monster.health -= WEAK_MONSTER_DAMAGE
    db.session.commit()
    return True