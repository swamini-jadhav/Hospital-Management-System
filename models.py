from app import db

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String, nullable=False)
#     username = db.Column(db.String, unique=True, nullable=False)
#     password = db.Column(db.String, nullable=False)

class Appointment(db.Model):
    AppointmentID = db.Column(db.Integer, primary_key=True)
    PatientID = db.Column(db.Integer)
    DoctorID = db.Column(db.Integer)
    Date=db.Column(db.Date)
    Time=db.Column(db.Time)
    Purpose=db.Column(db.String)
    Status=db.Column(db.Enum("Booked","Completed","Cancelled"),
        nullable=False,
        default='Booked'
    )

class Patient(db.Model):
    PatientID = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.String,nullable=False)
    LastName = db.Column(db.String,nullable=False)
    Username= db.Column(db.String, nullable=False)
    Password = db.Column(db.String, nullable=False)

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
    #available=db.Column(db.JSON)

    Position = db.Column(db.String)
    Experience = db.Column(db.Integer)
    Remarks = db.Column(db.String)
    photo = db.Column(db.String)

class PatientHistory(db.Model):
    AppointmentID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    PatientID = db.Column(db.Integer)
    DoctorID = db.Column(db.Integer)
    VisitType=db.Column(db.String,nullable=False)
    TestDone=db.Column(db.String)
    Diagnosis=db.Column(db.String,nullable=False)
    Prescription= db.Column(db.String,nullable=False)
    Medicines = db.Column(db.String,nullable=False)

