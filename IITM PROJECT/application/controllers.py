from flask import Flask, render_template, redirect, request
from flask import current_app as app #current_app refers to app.py
from .models import *

@app.route("/login", methods=["GET","post"])
def login():
    if request.method =="POST":
        username=request.form["username"]
        pwd=request.form["pwd"]
        this_user=User.query.filter_by(username=username).first()
        if this_user: #if the user exists
            if this_user.password==pwd:
                if this_user.type=="admin":
                    return redirect("/admin_dash")
                elif this_user.type=="doctor":
                    return redirect("/doctor_dash")
                else:
                    return render_template("patient_dash.html",this_user=this_user)
            else:
                return redirect("incorrect_p.html")
        else:
            return render_template("not_exist.html")
    return render_template("login.html")

@app.route("/register",methods=["GET","POST"])
def register():
    if request.method=="POST":
        username=request.form.get("username")
        email=request.form.get("email")
        pwd=request.form.get("pwd")
        fname=request.form.get("fname")
        age=request.form.get("age")
        gender=request.form.get("gender")
        contact=request.form.get("contact")
        user_name=User.query.filter_by(username=username).first()
        user_email=User.query.filter_by(email=email).first()
        if user_name or user_email:
            return render_template("already.html")
        else:
            new_user=User(username=username, email=email, password=pwd, type="patient")
            new_patient=Patient(username=username, password=pwd, full_name=fname, age=age, gender=gender, contact=contact)
            db.session.add(new_user) 
            db.session.add(new_patient)  
            db.session.commit()
            return redirect("/login")
    return render_template("register.html")

@app.route("/admin_dash")
def admin():
    this_user=User.query.filter_by(type="admin").first()
    doctors = Doctor.query.all()
    patients = Patient.query.all()
    appointments = (
        Appointment.query
        .join(Patient, Appointment.patient_id == Patient.id)
        .join(Doctor, Appointment.doctor_id == Doctor.id)
        .join(Department, Appointment.department_id == Department.id)
        .add_columns(
            Appointment.id.label("app_id"),
            Patient.full_name.label("patient_name"),
            Doctor.full_name.label("doctor_name"),
            Department.name.label("dept_name")
        ).all())
    return render_template(
        "admin_dash.html",
        this_user=this_user,
        doctors=doctors,
        patients=patients,
        appointments=appointments
    )
    
@app.route("/patient_dash/<int:id>")
def home(id):
    patient = Patient.query.filter_by(id=id).first()
    departments = Department.query.all()
    upcoming_appointments = (
        Appointment.query
        .filter_by(patient_id=patient.id)
        .filter(Appointment.date >= date.today())         # only future appointments
        .join(Doctor, Appointment.doctor_id == Doctor.id)
        .join(Department, Appointment.department_id == Department.id)
        .add_columns(
            Appointment.id.label("app_id"),
            Doctor.full_name.label("doctor_name"),
            Department.name.label("dept_name"),
            Appointment.date.label("date"),
            Appointment.time_slot.label("time")
        ).all())
    return render_template(
        "patient_dash.html",
        patient=patient,
        departments=departments,
        appointments=upcoming_appointments
    )
    
@app.route("/edit_doctor/<int:id>", methods=["GET", "POST"])
def edit_doctor(id):
    doctor = Doctor.query.filter_by(id=id).first()
    departments = Department.query.all()

    if request.method == "POST":
        doctor.full_name = request.form["name"]
        doctor.department_id = request.form["dept"]
        doctor.experience = request.form["experience"]
        db.session.commit()
        return redirect("/admin_dash")

    return render_template(
        "edit_doctor.html",
        doctor=doctor,
        departments=departments
    )

@app.route("/admin_dash/delete/<int:id>")
def delete_doctor(id):
    doctor = Doctor.query.filter_by(id=id).first()
    if not doctor:
        return "Doctor not found", 404

    Appointment.query.filter_by(doctor_id=id).delete()
    DoctorAvailability.query.filter_by(doctor_id=id).delete()


    db.session.delete(doctor)
    db.session.commit()
    
    return redirect("/admin_dash")  # Redirect back to the dashboard

@app.route('/admin_dash/delete/<int:id>', methods=['GET'])
def del_patient(id):
    patient = Patient.query.filter_by(id=id)
    
    Appointment.query.filter_by(id=id).delete()


    db.session.delete(patient)
    db.session.commit()

    return redirect("/admin_dashboard")


@app.route("/admin_dash/add_doctor", methods=["GET", "POST"])
def add_doctor():
    if request.method == "POST":
        id=request.form.get("id")
        username=request.form.get("username")
        pwd=request.form.get("pwd")
        fname=request.form.get("fname")
        did=request.form.get("did")
        experience=request.form.get("experience")
        specialization=request.form.get("specialization")
        qualification=request.form.get("qualifications")

        new_doc = Doctor(
            id=id,
            username=username,
            full_name=fname,
            specialization=specialization,
            experience=experience,
            password=pwd,
            department_id=did,
            qualification=qualification
            
        )

        db.session.add(new_doc)
        db.session.commit()

        return redirect("/admin_dash")

    return render_template("add_doctor.html")

