from .database import db #.database means looking for the current directory, and just directory means searchin in the root directory, and appln.db will make models.py think there is another appln folder wrt models
from sqlalchemy.orm import relationship
from datetime import date


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    email=db.Column(db.String(), nullable=False)
    type=db.Column(db.String(), nullable=False, default="user")
    
class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)

    full_name = db.Column(db.String(), nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.String())
    contact = db.Column(db.String())
    
    appointments = relationship("Appointment", back_populates="patient")
    histories = relationship("PatientHistory", back_populates="patient")
    
class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    full_name = db.Column(db.String(), nullable=False)

    specialization = db.Column(db.String()) 
    department_id = db.Column(db.Integer, db.ForeignKey("department.id"))

    experience = db.Column(db.Integer)
    qualification = db.Column(db.String())

    appointments = relationship("Appointment", back_populates="doctor")
    histories = relationship("PatientHistory", back_populates="doctor")
    availability = relationship("DoctorAvailability", back_populates="doctor")

class PatientHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    patient_id = db.Column(db.Integer, db.ForeignKey("patient.id"))
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctor.id"))

    visit_date = db.Column(db.Date, nullable=False)
    visit_type = db.Column(db.String(20))       # in-person / virtual
    test_done = db.Column(db.String(120))
    diagnosis = db.Column(db.Text)
    prescription = db.Column(db.Text)
    medicines = db.Column(db.String(255))       # "med1 1-0-1, med2 0-1-1"

    patient = relationship("Patient", back_populates="histories")
    doctor = relationship("Doctor", back_populates="histories")
    
class Appointment(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    patient_id = db.Column(db.Integer, db.ForeignKey("patient.id"))
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctor.id"))

    department_id = db.Column(db.Integer, db.ForeignKey("department.id"))

    visit_type = db.Column(db.String(20))  # in-person / online
    date = db.Column(db.Date)
    time_slot = db.Column(db.String(50))    # "9:00 am - 12:00 pm"

    status = db.Column(db.String(20), default="scheduled")

    patient = relationship("Patient", back_populates="appointments")
    doctor = relationship("Doctor", back_populates="appointments")
    
class Department(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    overview = db.Column(db.Text)

    doctors = relationship("Doctor", backref="department")
    
class DoctorAvailability(db.Model):
    __tablename__ = "doctor_availability"

    id = db.Column(db.Integer, primary_key=True)

    doctor_id = db.Column(db.Integer, db.ForeignKey("doctor.id"))

    date = db.Column(db.Date, nullable=False)

    slot_1 = db.Column(db.Boolean, default=False)  # 09:00-12:00
    slot_2 = db.Column(db.Boolean, default=False)  # 12:00-03:00

    doctor = relationship("Doctor", back_populates="availability")





