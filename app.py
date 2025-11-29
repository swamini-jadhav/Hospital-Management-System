from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = "your-secret-key"

BASE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE, "HMS.sqlite3")

app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_PATH}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from models import db, Admin, Department

db.init_app(app)

with app.app_context():
    db.create_all()  
    existing_admin = Admin.query.filter_by(Username="admin@email.com").first()
    if not existing_admin:
        admin = Admin(
            FirstName="Super",
            LastName="Admin",
            Username="admin@email.com",
            Password="admin123"
        )
        
        d1 = Department(
            Department_name="Cardiology",
            Overview="Deals with disorders of the heart."
        )

        d2 = Department(
            Department_name="Neurology",
            Overview="Focuses on disorders of the nervous system."
        )
        db.session.add(admin)
        db.session.add(d1)
        db.session.add(d2)
        db.session.commit()

        print("Departments added!")
        print("✔ Default Admin Created: admin/admin123")
    else:
        print("✔ Admin already exists")


from routes.login import *
from routes.patient import *
from routes.appointment import *
from routes.doctor import *
from routes.admin import *

if __name__ == "__main__":
    app.run(debug=True)
