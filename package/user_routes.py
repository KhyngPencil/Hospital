import json
from functools import wraps
from werkzeug.security import generate_password_hash,check_password_hash
from flask import render_template,request,abort,redirect,flash,make_response,session,url_for,jsonify

#local Imports

from package import app,csrf
from package.models import db,Patient,Doctor,Specilaization,Appointments,Ailments,PatientAilments,Pregnancy
from package.forms import *


@app.after_request
def after_request(response):
    #TO solve teh problem of loggedout user's details being cached in the browser 
    response.headers['Cache-Control']="no-cache, no-store, must-revalidate"
    return response

def login_required(f):
    @wraps(f)
    def login_check(*args,**kwargs):
        if session.get('userloggedin')!=None:
            return f(*args,**kwargs)
        else:
            flash("Access Denied,Login To Gain Access")
            return redirect('/login')
    return login_check
        

@app.route('/',methods=['POST','GET'])
def home():
    config_items=app.config
    return render_template("/users/index2.html")

@app.route('/login',methods=['POST','GET'])
def patient_login():    
    log=LogForm()
    if request.method=='GET':
        return render_template('users/log.html',log=log)
    else:
        username= request.form.get('username')
        pwd= request.form.get('pwd')
        patientdeets= db.session.query(Patient).filter(Patient.username==username).first()
        if patientdeets != None:
            hashed_pwd=patientdeets.password
            if check_password_hash(hashed_pwd,pwd)==True:
                session['userloggedin']=patientdeets.user_id
                return redirect('/patient/dashboard')
            else:
                flash("Invalid Credentials,Try Again")
                return redirect('/login')
        else:
            flash("Invalid Login Credentials, Try Again")
            return redirect("/login")



        




@app.route('/appointment/',methods=['POST','GET'])
@login_required
def patient_appointment():
    id=session.get('userloggedin')    
    sesdeets=db.session.query(Patient).get(id)
    patdeets=Appointments.query.filter(Appointments.user_id==sesdeets.user_id,Appointments.status=='1').all()
    return render_template("/users/appointments.html",patdeets=patdeets)

@app.route('/declined_appointment/',methods=['POST','GET'])
@login_required
def patient_declined_appointment():
    id=session.get('userloggedin')    
    sesdeets=db.session.query(Patient).get(id)
    patdeets=Appointments.query.filter(Appointments.user_id==sesdeets.user_id,Appointments.status=='2').all()
    return render_template("/users/declined_appointments.html",patdeets=patdeets)


@app.route('/doctor_feedback/')
@login_required
def diagnosis_feedback():
    id=session.get('userloggedin')    
    sesdeets=db.session.query(Patient).get(id)
    patdeets=PatientAilments.query.filter(PatientAilments.patient_id==sesdeets.user_id).all()
    return render_template("/users/diagosis_feedback.html",patdeets=patdeets)



@app.route('/register/patient',methods=['POST','GET'])
def register():
    patreg=CreateAccount()
    if request.method =="GET":
        return render_template('users/reg.html',patreg=patreg)
    else:
        if patreg.validate_on_submit:
            fname=request.form.get('fname')
            lname=request.form.get('lname')
            phone=request.form.get('phn')
            address=request.form.get('address')
            dob=request.form.get('Dob')
            gen=request.form.get('gender')
            email=request.form.get('email')
            status=request.form.get('pregstatus')
            edd=request.form.get('EDD')
            # pregstatus=request.form.get('pregstatus')
            # edd=request.form.get('EDD')
            username=request.form.get('username')
            pwd=request.form.get('pwd')
            hashed_pwd=generate_password_hash(pwd)
            fulname=fname+" "+lname            
            user=Patient(fullname=fulname,date_of_birth=dob,phonenumber=phone,address=address,password=hashed_pwd,email=email,username=username,gender=gen)
            db.session.add(user)
            db.session.commit()
            flash("Account Created, Please Loggin")        
          
            if gen=='Female' and status=='1':
                pat=Pregnancy(edd=edd,status='1',pat_id=user.user_id)
                db.session.add(pat)
                db.session.commit()
                flash("Account Created, Please Loggin")            
            return redirect('/login')
        else:
            flash('Error From Db')
            return render_template('users/reg.html',patreg=patreg)
        



@app.route('/get_delivery_date', methods=['POST'])
def get_delivery_date():
    user_choice = request.json['user_choice']
    if user_choice == 'no':
        return jsonify({'show_date_input': True})
    else:
        return jsonify({'show_date_input': False})










@app.route('/bookappointments/',methods=['POST','GET'])
@login_required
def book_appointment():
        id=session.get('userloggedin')
        sesdeets=db.session.query(Patient).get(id)
        doc= db.session.query(Doctor).all()
        if request.method=='GET':
            return render_template('/users/bookappointment.html',doc=doc,sesdeets=sesdeets)
        else:
            if id!= None:
                docid=request.form.get('doctor')
                date=request.form.get('apdate')
                time=request.form.get('aptime')
                comp=request.form.get('comp')
                appoint=Appointments(user_id=sesdeets.user_id,appointments_date=date,doctor_id=docid,complaints=comp,appointments_time=time)
                db.session.add(appoint)
                db.session.commit()
                flash('Appointment Booked Successfully,Check Your Appointments To See Doctor Feedback ')
                return redirect('/patient/dashboard')
            else:
                flash('Error In Db')
                return render_template('/users/bookappointment.html',doc=doc,sesdeets=sesdeets)
        



@app.route('/logout')
def logout():
    if session.get("userloggedin")!= None:
        session.pop("userloggedin",None)
    return redirect('/') 





        
@app.route('/patient/dashboard')
@login_required
def patient_dashboard():
    id=session.get('userloggedin')
    userdeets=db.session.query(Patient).get_or_404(id)
    return render_template('users/patient_dashboard.html',userdeets=userdeets)


# @app.route('/pregnancy_form')
# @login_required
# def pregnacy_form():
#     preg=PregForm()
#     id=session.get('userloggedin')
#     if request.method=='GET':
#         return render_template('users/pregnancy_form.html')
#     else:
#         edd=request.form.get('edd')
#         pre=Pregnancy()


@app.errorhandler(404)
def page_not_found(error):
    return render_template('/users/error404.html',error=error),404

@app.errorhandler(403)
def forbidden(error):
    return render_template('/users/error404.html',error=error),403

@app.errorhandler(500)
def server_error(error):
    return render_template('/users/error404.html',error=error),500
