from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy 
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE, "HMS.sqlite3")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_PATH}"
db = SQLAlchemy(app)



# Models
class Patient(db.Model):
    PatientID = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.String,nullable=False)
    LastName = db.Column(db.String,nullable=False)
    Username= db.Column(db.String, nullable=False)
    Password = db.Column(db.String, nullable=False)

# Routes

if __name__ == "__main__":
    # Create tables if DB does not exist
    with app.app_context():
        db.create_all()

    app.run(debug=True)