from flask import render_template, request, redirect, url_for
from app import app, db
from models import Patient, Department, Appointment, Doctor,PatientHistory
from datetime import datetime, timedelta

@app.route('/patient_dashboard/<int:patientID>')
def patient_dashboard(patientID):
    # fetch data using the patientID
    patient = Patient.query.get(patientID)
    departments = Department.query.all()
    appointments = Appointment.query.filter(
    Appointment.PatientID == patientID,
    Appointment.Status == "Booked"
    ).all()
    return render_template("patient_dashboard.html", patient=patient, departments=departments,appointments=appointments)

@app.route("/view_patient_history/<int:patient_id>")
def view_patient_history(patient_id):

    patient = Patient.query.get_or_404(patient_id)

    history_entries = PatientHistory.query.filter_by(PatientID=patient_id).all()    
    doctor_map = {
        entry.DoctorID: Doctor.query.get(entry.DoctorID)
        for entry in history_entries
    }

    return render_template(
        "view_patient_history.html",
        patient=patient,
        history=history_entries,
        doctor_map=doctor_map
    )


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


@app.route("/doctor_info/<int:doctor_id>")
def doctor_info(doctor_id):
    doctor = Doctor.query.get(doctor_id)
    if not doctor:
        return "Doctor not found", 404
    return render_template("doctor_info.html", doctor=doctor)

@app.route('/edit_patient/<int:patient_id>', methods=['GET', 'POST'])
def edit_patient(patient_id):
    patient = Patient.query.get(patient_id)
    if request.method == 'POST':
        # Get updated form values
        patient.FirstName = request.form['FirstName']
        patient.LastName = request.form['LastName']
        patient.Username = request.form['Username']
        patient.Password = request.form['Password']  # hashing recommended
        db.session.commit()

    return render_template('edit_patient.html', patient=patient)