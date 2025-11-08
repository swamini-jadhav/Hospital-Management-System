from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy 
from app import app, db

@app.route("/make_appointment", methods=["GET", "POST"])
def regmake_appointment():
    
    days = [
        {"date": "21/01/2025", "morning": "08:00 - 12:00 am", "evening": "04:00 - 9:00 pm"},
        {"date": "22/01/2025", "morning": "08:00 - 12:00 am", "evening": "04:00 - 9:00 pm"},
        {"date": "23/01/2025", "morning": "08:00 - 12:00 am", "evening": "04:00 - 9:00 pm"},
        {"date": "24/01/2025", "morning": "08:00 - 12:00 am", "evening": "04:00 - 9:00 pm"},
        {"date": "25/01/2025", "morning": "08:00 - 12:00 am", "evening": "04:00 - 9:00 pm"},
        {"date": "26/01/2025", "morning": "08:00 - 12:00 am", "evening": "04:00 - 9:00 pm"},
        {"date": "27/01/2025", "morning": "08:00 - 12:00 am", "evening": "04:00 - 9:00 pm"}
    ]

    if request.method == "POST":
        department=request.form["Dept"]
        #doctors = Doctor.query.filter_by(dept=department).all()
        #Doctor_Names=[d.name for d in doctors]


    return render_template("make_appointment.html", message="Appointment Booked Successfully", days=days)


if __name__ == "__main__":
    # Create tables if DB does not exist
    with app.app_context():
        db.create_all()

    app.run(debug=True)