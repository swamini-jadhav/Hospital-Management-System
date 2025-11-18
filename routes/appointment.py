from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy 
from app import app, db
from datetime import datetime, timedelta, date
from models import Doctor, Appointment
# @app.route("/make_appointment", methods=["GET", "POST"])
# def regmake_appointment():
    
#     days = [
#         {"date": "21/01/2025", "morning": "08:00 - 12:00 am", "evening": "04:00 - 9:00 pm"},
#         {"date": "22/01/2025", "morning": "08:00 - 12:00 am", "evening": "04:00 - 9:00 pm"},
#         {"date": "23/01/2025", "morning": "08:00 - 12:00 am", "evening": "04:00 - 9:00 pm"},
#         {"date": "24/01/2025", "morning": "08:00 - 12:00 am", "evening": "04:00 - 9:00 pm"},
#         {"date": "25/01/2025", "morning": "08:00 - 12:00 am", "evening": "04:00 - 9:00 pm"},
#         {"date": "26/01/2025", "morning": "08:00 - 12:00 am", "evening": "04:00 - 9:00 pm"},
#         {"date": "27/01/2025", "morning": "08:00 - 12:00 am", "evening": "04:00 - 9:00 pm"}
#     ]

#     if request.method == "POST":
#         department=request.form["Dept"]
#         #doctors = Doctor.query.filter_by(dept=department).all()
#         #Doctor_Names=[d.name for d in doctors]


#     return render_template("make_appointment.html", message="Appointment Booked Successfully", days=days)
@app.route("/show_available/<int:doctor_id>/<doctor_available>/<int:patient_id>",
           methods=["GET", "POST"])
def show_available(doctor_id, doctor_available, patient_id):
    if request.method == "POST":
        chosen = request.form.get("selected_slot")
        purpose=request.form.get("purpose")
        if chosen:
            idx = int(chosen)   # direct integer slot index (0–13)
            updatedl= list(doctor_available)
            updatedl[idx]="0"
            updated="".join(updatedl)

            # Update DB
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
            Purpose = purpose,   # You can replace this with your form
            Status = "Booked"
            )
            db.session.add(new_apt)
            db.session.commit()
            return redirect(url_for("patient_dashboard", patientID=patient_id))
        


    #doctor_available = "01001111000010"
    availability = []
    for i in range(0, 14, 2):
        availability.append((int(doctor_available[i]), int(doctor_available[i+1])))
    # Now availability = [(m1, e1), (m2, e2), ... (m7, e7)]

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
