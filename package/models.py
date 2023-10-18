from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
db=SQLAlchemy()

class Patient(db.Model):
    user_id= db.Column(db.Integer(),primary_key=True,autoincrement=True)
    fullname=db.Column(db.String(60),nullable=False)
    gender=db.Column(db.String(60),nullable=False)
    email=db.Column(db.String(60),nullable=False)
    username=db.Column(db.String(60),nullable=False,unique=True)
    password=db.Column(db.String(200),nullable=False)
    address=db.Column(db.String(200),nullable=False)
    phonenumber=db.Column(db.String(60),nullable=False)
    date_of_birth=db.Column(db.DateTime(),default=datetime.utcnow)
    #setting relationships
    appoints=db.relationship("Appointments", backref="patientdeets",cascade="all, delete-orphan")  
    pregdeets=db.relationship("Pregnancy",backref="patdeets",cascade="all,delete-orphan")  
     #setting relationships
    pat_ali=db.relationship('PatientAilments',backref="patdeets",cascade="all, delete-orphan")


class Doctor(db.Model):
    doctor_id= db.Column(db.Integer(),primary_key=True,autoincrement=True)
    doctoraddress= db.Column(db.String(200),nullable=False)
    doctorphonenumber=db.Column(db.String(60),nullable=False)
    doctorfullname=db.Column(db.String(100),nullable=False)
    doctor_username=db.Column(db.String(60),nullable=False,unique=True)
    doctor_email=db.Column(db.String(150),nullable=False)
    doctor_password=db.Column(db.String(200),nullable=False)
    #setting foreign key
    doctor_specialization= db.Column(db.Integer(),db.ForeignKey('specilaization.specialization_id'))
    #setting relationships
    specs=db.relationship("Specilaization", backref="docdeets")
    appoints=db.relationship("Appointments", backref="docdeets",cascade="all, delete-orphan")
    pat_ali=db.relationship("PatientAilments", backref="docdeets",cascade="all, delete-orphan")

class PatientAilments(db.Model):
    id_patient_ailments= db.Column(db.Integer(),primary_key=True,autoincrement=True)
    advice=db.Column(db.String(500),nullable=False)
    diagnosis_date= db.Column(db.Date(),default=datetime.utcnow)     
    #setting foreign key
    patient_id= db.Column(db.Integer(),db.ForeignKey('patient.user_id'))
    ailment_id= db.Column(db.Integer(),db.ForeignKey('ailments.id_ailments'))
    doctor_id= db.Column(db.Integer(),db.ForeignKey('doctor.doctor_id'))



class Ailments(db.Model):
    id_ailments= db.Column(db.Integer(),primary_key=True,autoincrement=True)
    ailments= db.Column(db.String(60),nullable=False)
     #setting relationships
    pat_ail=db.relationship('PatientAilments',backref="aildeets")


class Pregnancy(db.Model):
    id_pregnancy=  db.Column(db.Integer(),primary_key=True,autoincrement=True)
    edd=db.Column(db.Date(),default=datetime.utcnow)
    pat_id=db.Column(db.Integer(),db.ForeignKey('patient.user_id'))
    status= db.Column(db.Enum('1','0'),nullable=False, server_default=("0"))  
    

class Specilaization(db.Model):
    specialization_id= db.Column(db.Integer(),primary_key=True,autoincrement=True)
    specialization= db.Column(db.String(60),nullable=False)
    #setting relationships
    



class Appointments(db.Model):
    appointments_id=  db.Column(db.Integer(),primary_key=True,autoincrement=True)
    appointments_date= db.Column(db.Date(),default=datetime.utcnow)
    appointments_time=db.Column(db.Time())
    status=  db.Column(db.Enum('1','0','2'),nullable=False, server_default=("0")) 
    Reasons=db.Column(db.String(450),nullable=True) 
    complaints= db.Column(db.String(450),nullable=False)
    
    #setting Foreign Key
    user_id= db.Column(db.Integer(),db.ForeignKey('patient.user_id'))
    doctor_id= db.Column(db.Integer(),db.ForeignKey('doctor.doctor_id'))
    #setting relationships
    

class Admin(db.Model):
    admin_id= db.Column(db.Integer(),primary_key=True,autoincrement=True)
    admin_username=db.Column(db.String(20),nullable=True)
    admin_pwd=db.Column(db.String(200),nullable=True)


