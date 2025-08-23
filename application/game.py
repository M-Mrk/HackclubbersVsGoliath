from .db import db, User, Monsters, Attacks
from datetime import datetime, timezone, timedelta

COOLDOWN = timedelta(hours=23) # 23 instead of 24 to avoid endless shifting
STRONG_MONSTER_DAMAGE = 10
WEAK_MONSTER_DAMAGE = 1

def get_attack_status(user_uuid):
    user = db.session.query(User).filter_by(uuid=user_uuid).one()
    if user.attacked_at:
        current_time = datetime.now(timezone.utc)
        user_attacked_time = user.attacked_at if user.attacked_at.tzinfo else user.attacked_at.replace(tzinfo=timezone.utc)
        if current_time - user_attacked_time > COOLDOWN:
            return True
        else:
            time_left = COOLDOWN - (current_time - user_attacked_time)
            return time_left
    return True

def attack_monster(damage):
    monster = db.session.query(Monsters).filter_by(active=True).one()
    monster.health -= damage
    db.session.commit()
    if monster.health <= 0:
        monster.active = False
        monster.defeated_at = datetime.now(timezone.utc)
        db.session.commit()
        new_monster = db.session.query(Monsters).filter_by(active=False, defeated_at=None).first()
        if new_monster:
            new_monster.active = True

def attack_strong_monster(user_uuid):
    user = db.session.query(User).filter_by(uuid=user_uuid).one()
    if get_attack_status(user_uuid) == True:
        monster = db.session.query(Monsters).filter_by(active=True).one()
        attack_monster(STRONG_MONSTER_DAMAGE)
        current_time = datetime.now(timezone.utc)
        attack = Attacks(
            user_id=user.id, 
            monster_id=monster.id, 
            damage=STRONG_MONSTER_DAMAGE, 
            attack_type="strong",
            created_at=current_time
        )
        db.session.add(attack)
        user.attacked_at = current_time
        db.session.commit()
        return True
    return False

def attack_weak_monster(user_uuid):
    user = db.session.query(User).filter_by(uuid=user_uuid).one()
    monster = db.session.query(Monsters).filter_by(active=True).one()
    attack_monster(WEAK_MONSTER_DAMAGE)
    current_time = datetime.now(timezone.utc)
    attack = Attacks(
        user_id=user.id, 
        monster_id=monster.id, 
        damage=WEAK_MONSTER_DAMAGE, 
        attack_type="weak",
        created_at=current_time
    )
    db.session.add(attack)
    db.session.commit()
    return True