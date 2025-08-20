from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(50), nullable=False)
    attacked = db.Column(db.Boolean, default=False)
    small_attacks = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

class Monsters(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    health = db.Column(db.Integer, default=100)
    attack_power = db.Column(db.Integer, default=3)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    active = db.Column(db.Boolean, default=False)
    defeated_at = db.Column(db.DateTime, nullable=True)