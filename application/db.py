from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

db = SQLAlchemy()

def utcnow():
    return datetime.now(timezone.utc)

class Attacks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    monster_id = db.Column(db.Integer, db.ForeignKey('monsters.id'), nullable=False)
    damage = db.Column(db.Integer, nullable=False)
    attack_type = db.Column(db.String(10), nullable=False)
    created_at = db.Column(db.DateTime, default=utcnow)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(50), nullable=False)
    uuid = db.Column(db.String(36), unique=True, nullable=False)
    attacked_at = db.Column(db.DateTime, nullable=True)
    small_attacks = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=utcnow)

class Monsters(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    health = db.Column(db.Integer, default=100)
    max_health = db.Column(db.Integer, default=100)
    attack_power = db.Column(db.Integer, default=3)
    created_at = db.Column(db.DateTime, default=utcnow)
    active = db.Column(db.Boolean, default=False)
    defeated_at = db.Column(db.DateTime, nullable=True)
    url = db.Column(db.String(200), nullable=True)