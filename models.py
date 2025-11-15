from app import db

class Appointment(db.Model):
    AppointmentID = db.Column(db.Integer, primary_key=True)
    PatientID = db.Column(db.Integer, db.ForeignKey('patient.PatientID'), nullable=False)
    DoctorID = db.Column(db.Integer, db.ForeignKey('doctor.DoctorID'), nullable=False)
    Date=db.Column(db.Date)
    Time=db.Column(db.Time)
    Purpose=db.Column(db.String)
    Status=db.Column(db.Enum("Booked","Completed","Cancelled"),
        nullable=False,
        default='Booked'
    )
    patient = db.relationship('Patient', back_populates='appointments')
    doctor = db.relationship('Doctor', back_populates='appointments')

class Patient(db.Model):
    PatientID = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.String,nullable=False)
    LastName = db.Column(db.String,nullable=False)
    Username= db.Column(db.String, nullable=False)
    Password = db.Column(db.String, nullable=False)

    appointments = db.relationship('Appointment', back_populates='patient', cascade="all, delete")
    histories = db.relationship('PatientHistory', back_populates='patient', cascade="all, delete")

class Admin(db.Model):
    AdminID = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.String,nullable=False)
    LastName = db.Column(db.String,nullable=False)
    Username= db.Column(db.String, nullable=False)
    Password = db.Column(db.String, nullable=False)

class Doctor(db.Model):
    DoctorID = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.String,nullable=False)
    LastName = db.Column(db.String,nullable=False)
    Username= db.Column(db.String, nullable=False)
    Password = db.Column(db.String, nullable=False)
    available=db.Column(db.String)
    
    Department = db.Column(db.String, db.ForeignKey('department.Department_name'), nullable=False)
    Position = db.Column(db.String)
    Experience = db.Column(db.Integer)
    Remarks = db.Column(db.String)
    photo = db.Column(db.String)

    appointments = db.relationship('Appointment', back_populates='doctor', cascade="all, delete")
    department_rel = db.relationship('Department', back_populates='doctors')

class PatientHistory(db.Model):
    AppointmentID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    PatientID = db.Column(db.Integer, db.ForeignKey('patient.PatientID'), nullable=False)
    DoctorID = db.Column(db.Integer)
    VisitType=db.Column(db.String,nullable=False)
    TestDone=db.Column(db.String)
    Diagnosis=db.Column(db.String,nullable=False)
    Prescription= db.Column(db.String,nullable=False)
    Medicines = db.Column(db.String,nullable=False)

    patient = db.relationship('Patient', back_populates='histories')


class Department(db.Model):
    Department_name=db.Column(db.String, primary_key=True)
    Overview = db.Column(db.String)
    doctors = db.relationship('Doctor', back_populates='department_rel', cascade="all, delete")

