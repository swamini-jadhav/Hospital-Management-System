from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy 
import os

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(BASE, "HMS.sqlite3")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_PATH}"
db = SQLAlchemy(app)



# Models
class Appointment(db.Model):
    AppointmentID = db.Column(db.Integer, primary_key=True)
    PatientID = db.Column(db.Integer)
    DoctorID = db.Column(db.Integer)
    Date=db.Column(db.Date)
    Time=db.Column(db.Time)
    Purpose=db.Column(db.String)
    Status=db.Column(db.Enum("Booked","Completed","Cancelled"),
        nullable=False,
        default='Booked'
    )
    


# Routes



@app.route("/make_appointment", methods=["GET", "POST"])
def regmake_appointment():

    if request.method == "POST":
        department=request.form["Dept"]
        #doctors = Doctor.query.filter_by(dept=department).all()
        #Doctor_Names=[d.name for d in doctors]


    return render_template("make_appointment.html", message="Appointment Booked Successfully")


if __name__ == "__main__":
    # Create tables if DB does not exist
    with app.app_context():
        db.create_all()

    app.run(debug=True)