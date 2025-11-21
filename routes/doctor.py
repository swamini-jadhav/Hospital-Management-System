from flask import render_template, request, redirect, url_for
from app import app, db
from models import Patient, Department, Appointment, Doctor,PatientHistory
from datetime import datetime, timedelta

@app.route('/doctor_dashboard/<int:doctorID>')
def doctor_dashboard(doctorID):
    # fetch data using the patientID
    doctor = Doctor.query.get(doctorID)
    appointments = Appointment.query.filter(
    Appointment.DoctorID == doctorID,
    Appointment.Status != "Cancelled"
    ).all()
    patient_map = {
        entry.PatientID: Patient.query.get(entry.PatientID)
        for entry in appointments
    }
    patient_ids = {appt.PatientID for appt in appointments}
    assigned_patients = Patient.query.filter(Patient.PatientID.in_(patient_ids)).all()
    return render_template("doctor_dashboard.html", doctor=doctor,appointments=appointments, patient_map=patient_map, assigned_patients=assigned_patients)

@app.route("/update_patient_history/<int:doctor_id>/<int:patient_id>", methods=["GET", "POST"])
def update_history(doctor_id, patient_id):
    message =""
    patient = Patient.query.get(patient_id)
    if request.method == "POST":
        visit_type = request.form["visit_type"]
        test_done = request.form["test_done"]
        diagnosis =request.form["diagnosis"]
        prescription=request.form["prescription"]
        medicine=request.form["medicine"]

        new_apt = PatientHistory(
            PatientID=patient_id,
            DoctorID=doctor_id,
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
    return render_template("update_patient_history.html", patient=patient, message=message)

@app.route("/cancel_doctor_appointment/<int:appt_id>")
def cancel_doctor_appointment(appt_id):
    appt = Appointment.query.get(appt_id)
    if appt:
        appt.Status = "Cancelled"
        db.session.commit()

    return redirect(url_for("doctor_dashboard", doctorID=appt.DoctorID))


