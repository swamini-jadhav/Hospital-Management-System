from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy 
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE, "HMS.sqlite3")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_PATH}"
db = SQLAlchemy(app)
 #Add Jinja 2 Contnet Patient ID, Appointment ID etc


# Models
class PatientHistory(db.Model):
    AppointmentID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    PatientID = db.Column(db.Integer)
    DoctorID = db.Column(db.Integer)
    VisitType=db.Column(db.String,nullable=False)
    TestDone=db.Column(db.String)
    Diagnosis=db.Column(db.String,nullable=False)
    Prescription= db.Column(db.String,nullable=False)
    Medicines = db.Column(db.String,nullable=False)

# Routes
@app.route("/update_patient_history", methods=["GET", "POST"])
def updateHistory():
    message =""
    if request.method == "POST":
        visit_type = request.form["visit_type"]
        test_done = request.form["test_done"]
        diagnosis =request.form["diagnosis"]
        prescription=request.form["prescription"]
        medicine=request.form["medicines"]

        new_apt = PatientHistory(
            PatientID=123,
            DoctorID=456,
            VisitType=visit_type,
            TestDone=test_done,
            Diagnosis=diagnosis,
            Prescription=prescription,
            Medicines=medicine
        )

        db.session.add(new_apt)
        print("Received:", visit_type, test_done, diagnosis, prescription, medicine)
        db.session.commit()
        message = "Saved Successfully"
    return render_template("update_patient_history.html", message=message)

if __name__ == "__main__":
    # Create tables if DB does not exist
    with app.app_context():
        db.create_all()

    app.run(debug=True)