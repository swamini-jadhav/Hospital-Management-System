from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

BASE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE, "HMS.sqlite3")

app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_PATH}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


from routes.login import *
from routes.update_history import *

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
