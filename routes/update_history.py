from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy 
import os
from app import app, db
from models import PatientHistory


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
