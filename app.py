from flask import Flask, render_template, request, jsonify, session, url_for
from application.db import db
import os
import uuid
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

def prepare_uuid(ip):
    session.permanent = True
    if not session.get('uuid'):
        session['uuid'] = str(uuid.uuid4())
        from application.db_services import register_user
        register_user(uuid=session['uuid'], ip=ip)
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

if __name__ == "__main__":
    app.run(debug=True)
