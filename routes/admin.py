from flask import Flask, render_template, redirect, url_for, session, request
from models import Department, Doctor, Patient, Appointment, Admin
from app import db, app

@app.route("/admin_dashboard/<int:adminID>")
def admin_dashboard(adminID):
    patients = Patient.query.all()
    doctors = Doctor.query.all()
    appointments = Appointment.query.filter(
    Appointment.Status == "Booked"
    ).all()
    patient_map = {
        entry.PatientID: Patient.query.get(entry.PatientID)
        for entry in appointments
    }
    admin = Admin.query.get(adminID)

    return render_template("admin_dashboard.html", patients=patients, doctors=doctors, appointments=appointments, admin=admin)

@app.route("/delete_doctor/<int:id>/<int:adminID>")
def delete_doctor(id, adminID):
    doctor = Doctor.query.get_or_404(id)
    db.session.delete(doctor)
    db.session.commit()
    return redirect(url_for("admin_dashboard", adminID=adminID))

@app.route("/delete_patient/<int:id>/<int:adminID>")
def delete_patient(id, adminID):
    patient = Patient.query.get_or_404(id)
    db.session.delete(patient)
    db.session.commit()
    return redirect(url_for("admin_dashboard", adminID=adminID))


@app.route("/add_doctor", methods=["GET", "POST"])
def add_doctor():
    if request.method == "POST":
        fullname = request.form["fullname"]
        specialization = request.form["specialization"]
        experience = request.form["experience"]
        username = request.form["username"]
        password = request.form["password"]

        
        try:
            first, last = fullname.split(" ", 1)
        except:
            first = fullname
            last = ""

        new_doc = Doctor(
            FirstName=first,
            LastName=last,
            Username=username,
            Password=password,
            Department=specialization,
            Experience=experience,
            available="00000000000000",     
            Position="Doctor",   
            Remarks="",
            photo=""
        )

        db.session.add(new_doc)
        db.session.commit()

    return render_template("doctor_add.html")

@app.route('/search', methods=['GET', 'POST'])
def search():
    query = request.args.get('q') or request.form.get('q')

    q = f"%{query}%"
    doctor_results = Doctor.query.filter(
        (Doctor.FirstName.ilike(q)) |
        (Doctor.LastName.ilike(q)) |
        (Doctor.Username.ilike(q)) |
        (Doctor.Department.ilike(q))
    ).all()

    patient_results = Patient.query.filter(
        (Patient.FirstName.ilike(q)) |
        (Patient.LastName.ilike(q)) |
        (Patient.Username.ilike(q))
    ).all()

    department_results = Department.query.filter(
        Department.Department_name.ilike(q)
    ).all()

    return render_template(
        'search.html',
        query=query,
        doctors=doctor_results,
        patients=patient_results,
        departments=department_results
    )


