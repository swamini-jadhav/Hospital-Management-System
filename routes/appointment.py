from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy 
from app import app, db
from datetime import datetime, timedelta, date
from models import Doctor, Appointment

@app.route("/make_appointment/<int:doctor_id>/<doctor_available>/<int:patient_id>",
           methods=["GET", "POST"])
def make_appointment(doctor_id, doctor_available, patient_id):
    if request.method == "POST":
        chosen = request.form.get("selected_slot")
        purpose=request.form.get("purpose")
        if chosen:
            idx = int(chosen) 
            updatedl= list(doctor_available)
            updatedl[idx]="0"
            updated="".join(updatedl)

            doc = Doctor.query.get(doctor_id)
            doc.available = updated
            db.session.commit()

            appointment_date = datetime.today().date() + timedelta(days=idx)
            appointment_time = "08:00 - 12:00 am" if idx%2==0 else "04:00 - 09:00 pm"
            new_apt = Appointment(
            PatientID = patient_id,
            DoctorID = doctor_id,
            Date = appointment_date,
            Time = appointment_time,
            Purpose = purpose, 
            Status = "Booked"
            )
            db.session.add(new_apt)
            db.session.commit()
            return redirect(url_for("patient_dashboard", patientID=patient_id))
    availability = []
    for i in range(0, 14, 2):
        availability.append((int(doctor_available[i]), int(doctor_available[i+1])))
    today = datetime.today()
    days = []
    for i in range(1, 8):
        date = today + timedelta(days=i)
        days.append({
            "date": date.strftime("%d/%m/%Y"),
            "morning": "08:00 - 12:00 am",
            "evening": "04:00 - 09:00 pm"
        })

    return render_template("make_appointment.html",
                           days=days,
                           availability=availability,
                           message=None)

@app.route("/complete_appointment/<int:appt_id>")
def complete_appointment(appt_id):
    appt = Appointment.query.get(appt_id)
    if appt:
        appt.Status = "Completed"
        db.session.commit()

    return redirect(url_for("patient_dashboard", patientID=appt.PatientID))

@app.route("/complete_doctor_appointment/<int:appt_id>")
def complete_doctor_appointment(appt_id):
    appt = Appointment.query.get(appt_id)
    if appt:
        appt.Status = "Completed"
        db.session.commit()
    return redirect(url_for("doctor_dashboard", doctorID=appt.DoctorID))

@app.route("/cancel_appointment/<int:appt_id>")
def cancel_appointment(appt_id):
    appt = Appointment.query.get(appt_id)
    if appt:
        appt.Status = "Cancelled"
        db.session.commit()

    return redirect(url_for("patient_dashboard", patientID=appt.PatientID))

@app.route("/cancel_doctor_appointment/<int:appt_id>")
def cancel_doctor_appointment(appt_id):
    appt = Appointment.query.get(appt_id)
    if appt:
        appt.Status = "Cancelled"
        db.session.commit()

    return redirect(url_for("doctor_dashboard", doctorID=appt.DoctorID))

@app.route("/doctor_availability/<int:doctor_id>", methods=["GET", "POST"])
def doctor_availability(doctor_id):
    doctor = Doctor.query.get(doctor_id)
    current = doctor.available or "00000000000000"
    today = datetime.today()
    days = [(today + timedelta(days=i)).strftime("%d/%m/%Y") for i in range(1, 8)]
    availability = []

    for i in range(0, 14, 2):
        m = int(current[i])
        e = int(current[i+1])
        day = days[i//2]
        availability.append((day, (m, e)))

    if request.method == "POST":
        updated = []

        for idx in range(7):  
            m = "1" if request.form.get(f"slot{idx}m") else "0"
            e = "1" if request.form.get(f"slot{idx}e") else "0"
            updated.append(m)
            updated.append(e)

        updated_string = "".join(updated)
        doctor.available = updated_string
        db.session.commit()

        return redirect(url_for("doctor_dashboard", doctorID=doctor_id))

    return render_template("doctor_availability.html",
                           doctor=doctor,
                           availability=availability)




