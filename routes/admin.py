from flask import Flask, render_template, redirect, url_for, session, request
from models import Department, Doctor, Patient, PatientHistory, Appointment, Admin
from app import db, app

@app.route("/admin_dashboard/<int:adminID>")
def admin_dashboard(adminID):
    patients = Patient.query.all()
    doctors = Doctor.query.all()
    appointments = Appointment.query.all()
    admin = Admin.query.get(adminID)

    return render_template("admin_dashboard.html", patients=patients, doctors=doctors, appointments=appointments, admin=admin)

@app.route("/delete_doctor/<int:id>")
def delete_doctor(id):
    doctor = Doctor.query.get_or_404(id)
    db.session.delete(doctor)
    db.session.commit()
    return redirect(url_for("admin_dashboard", adminId=session.get("adminId")))

@app.route("/add_doctor", methods=["GET", "POST"])
def add_doctor():
    if request.method == "POST":
        fullname = request.form["fullname"]
        specialization = request.form["specialization"]
        experience = request.form["experience"]

        # Split first and last name
        try:
            first, last = fullname.split(" ", 1)
        except:
            first = fullname
            last = ""

        # Auto-create username & password
        username = (first + "." + last).lower() or first.lower()
        password = first.lower() + "123"   # you can hash this later

        new_doc = Doctor(
            FirstName=first,
            LastName=last,
            Username=username,
            Password=password,
            Department=specialization,
            Experience=experience,
            available="11111111111111",     # default
            Position="Doctor",   # default
            Remarks="",
            photo=""
        )

        db.session.add(new_doc)
        db.session.commit()

    return render_template("doctor_add.html")

