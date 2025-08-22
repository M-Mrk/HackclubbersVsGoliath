from flask import Flask, render_template, request, jsonify, session, url_for
from application.db import db
import os
from dotenv import load_dotenv
from flask_migrate import Migrate

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("FLASK_SECRET_KEY")

# PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@localhost:5432/{os.getenv('POSTGRES_DB')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate = Migrate(app, db)

def get_app():
    return app

def prepare_uuid(ip):
    from application.db_services import get_uuid
    session.permanent = True
    if not session.get('uuid'):
        session['uuid'] = get_uuid(ip=ip)
    return session['uuid']

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/monster", methods=["GET"])
def get_monster_info():
    from application.db_services import get_monster
    monster = get_monster()
    if monster:
        return jsonify({ "health": monster.health, "max_health": monster.max_health, "name": monster.name, "url": url_for('static', filename=f'{monster.url}') }), 200
    return jsonify({ "error": "Monster not found" }), 404

@app.route("/api/attack", methods=["POST", "GET"])
def attack_monster():
    user_uuid = prepare_uuid(ip=request.remote_addr)
    if request.method == "GET":
        from application.game import get_attack_status
        status = get_attack_status(user_uuid)
        if status == True:
            return jsonify({ "status": "ready" }), 200
        else:
            cooldown = status.total_seconds() / 3600
            rounded_cooldown = round(cooldown, 2)
            return jsonify({ "status": "on cooldown", "time_left": rounded_cooldown }), 200
    elif request.method == "POST":
        from application.game import attack_strong_monster, attack_weak_monster
        attack_type = request.json.get("type")
        if attack_type == "strong":
            success = attack_strong_monster(user_uuid)
        elif attack_type == "weak":
            success = attack_weak_monster(user_uuid)
        else:
            return jsonify({ "error": "Invalid attack type" }), 400
        
        if success:
            return jsonify({ "status": "attack successful" }), 200
        else:
            return jsonify({ "error": "Attack failed" }), 500

if __name__ == "__main__":
    app.run(debug=True)
