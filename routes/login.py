from flask import render_template, request, redirect, url_for
from app import app, db
from models import Patient, Doctor, Admin

@app.route("/", methods=["GET", "POST"])
def login():
    message = ""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        ChkDoc = Doctor.query.filter_by(Username=username, Password=password).first()
        ChkPat = Patient.query.filter_by(Username=username, Password=password).first()
        message = "Login successful!" if ChkDoc or ChkPat else "Invalid username or password"
        # if ChkDoc:
        #     return render_template("doctor_dashboard.html", Name=ChkDoc.DoctorID)
        if ChkPat:
            # return render_template("patient_dashboard.html", Name=ChkPat.PatientID)
            return redirect(url_for("patient_dashboard", patientID=ChkPat.PatientID))


    return render_template("login.html", message=message)

@app.route("/register", methods=["GET", "POST"])
def register():
    message = ""
    if request.method == "POST":
        name = request.form["name"]
        username = request.form["username"]
        password = request.form["password"]

        if Patient.query.filter_by(Username=username).first():
            message = "Username already exists"
        else:
            new_user = Patient(FirstName=name, LastName="XYZ", Username=username, Password=password)
            db.session.add(new_user)
            db.session.commit()
            message = "Registration successful!"

    return render_template("register.html", message=message)
