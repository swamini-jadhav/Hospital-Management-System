from flask import render_template, request, redirect, url_for
from app import app, db
from models import Patient, Department, Appointment, Doctor
from datetime import datetime, timedelta

@app.route('/patient_dashboard/<int:patientID>')
def patient_dashboard(patientID):
    # fetch data using the patientID
    patient = Patient.query.get(patientID)
    departments = Department.query.all()
    return render_template("patient_dashboard.html", patient=patient, departments=departments)

@app.route('/department/<dept_name>/<int:patient_id>')
def view_department(dept_name, patient_id):
    department = Department.query.get(dept_name)
    if not department:
        return "Department not found", 404
    patient = Patient.query.get(patient_id)
    if not patient:
        return "Patient not found", 404
    doctors = department.doctors   
    return render_template("view_department.html", department=department, doctors=doctors, patient=patient)


@app.route("/make_appointment/<int:patient_id>/<int:doctor_id>", methods=["GET", "POST"])
def make_appointment(patient_id, doctor_id):
    today = datetime.today()
    days = []
    for i in range(1, 8):
        date = today + timedelta(days=i)
        days.append({
            "date": date.strftime("%d/%m/%Y"),
            "morning": "08:00 - 12:00 am",
            "evening": "04:00 - 09:00 pm"
        })
    
    patient = Patient.query.get(patient_id)

    message = None  # default (don’t show message unless POST)

    if request.method == "POST":
        selected_slots = []
        for i in range(1, 8):
            if request.form.get(f"morning_{i}"):
                selected_slots.append(f"Morning of {days[i-1]['date']}")
            if request.form.get(f"evening_{i}"):
                selected_slots.append(f"Evening of {days[i-1]['date']}")
        
        print("Selected Slots:", selected_slots)
        message = "Appointment Booked Successfully ✅"

    return render_template("make_appointment.html", message=message, days=days, patient=patient)



@app.route("/doctor_info/<int:doctor_id>")
def doctor_info(doctor_id):
    doctor = Doctor.query.get(doctor_id)
    if not doctor:
        return "Doctor not found", 404
    return render_template("doctor_info.html", doctor=doctor)
    