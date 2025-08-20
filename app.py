from flask import Flask, render_template, request, jsonify
from application.db import db
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("FLASK_SECRET_KEY")

# PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@localhost:5432/{os.getenv('POSTGRES_DB')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
