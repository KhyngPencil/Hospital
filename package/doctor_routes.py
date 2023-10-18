import json
from functools import wraps
from werkzeug.security import generate_password_hash,check_password_hash
from flask import render_template,request,abort,redirect,flash,make_response,session,url_for

#local Imports

from package import app,csrf
from package.models import db,Patient,Doctor,Specilaization,Appointments,Ailments,PatientAilments,Pregnancy
from package.forms import *


def login_required(f):
    @wraps(f)
    def login_check(*args,**kwargs):
        if session.get('docloggedin')!=None:
            return f(*args,**kwargs)
        else:
            flash("Access Denied,Login To Gain Access")
            return redirect('/login/doc/')
    return login_check

@app.after_request
def after_request(response):
    #TO solve teh problem of loggedout user's details being cached in the browser 
    response.headers['Cache-Control']="no-cache, no-store, must-revalidate"
    return response

@app.route('/login/doc/',methods=['POST','GET'])
def doclogin():
    doc=DocLogForm()
    if request.method =="GET":    
        return render_template("/users/doclog.html",doc=doc)
    else:
        docmail=request.form.get('docemail')
        docpwd=request.form.get('docpwd')
        docs=db.session.query(Doctor).filter(Doctor.doctor_email==docmail).first()
        if docs!=None:
            hashed_pwd=docs.doctor_password
            if check_password_hash(hashed_pwd,docpwd)==True:
                session['docloggedin']=docs.doctor_id
                return redirect('/doctor/dashboard')
            else:
                flash('Invalid Credentials ')
                return render_template("/users/doclog.html",doc=doc)

        else:
            flash("Invalid Credentials,Try Again")
            return redirect("/login/doc/")
        
        
@app.route('/register/doctor',methods=["POST","GET"])
def docreg():    
    reg=RegForm()
    spec= db.session.query(Specilaization).all()
    if request.method=='GET':
        return render_template("/users/docreg.html",reg=reg,spec=spec)
    else:
        if reg.validate_on_submit:
            fname=request.form.get('fname')
            lname=request.form.get('lname')
            dpt=request.form.get('department')
            email=request.form.get('usermail')
            username=request.form.get('username')
            pwd=request.form.get('pwd')
            phone=request.form.get('phone')
            address=request.form.get('address')
            fullname= fname+" "+lname
            hashed_pwd=generate_password_hash(pwd)
            doc=Doctor(doctorfullname=fullname,doctor_email=email,doctor_password=hashed_pwd,doctorphonenumber=phone,doctoraddress=address,doctor_username=username,doctor_specialization=dpt)
            db.session.add(doc)
            db.session.commit()
            return redirect('/login/doc')
        else:
            return render_template("/users/docreg.html",reg=reg,doc=doc)
        

@app.route('/appointments/',methods=['POST','GET'])
@login_required
def doc_appointment():
    id=session.get('docloggedin')    
    sesdeets=db.session.query(Doctor).get(id)
    docdeets=Appointments.query.filter(Appointments.doctor_id==sesdeets.doctor_id,Appointments.status=='0').all()
    return render_template("/users/doctor_appointment.html", docdeets=docdeets,id=id)


@app.route('/approvedappointments/',methods=['POST','GET'])
@login_required
def doc_approvedappointment():
    id=session.get('docloggedin')    
    sesdeets=db.session.query(Doctor).get(id)
    docdeets=Appointments.query.filter(Appointments.doctor_id==sesdeets.doctor_id,Appointments.status=='1').all()
    return render_template("/users/doctor_approvedappointment.html", docdeets=docdeets,id=id)


@app.route('/doc/approve_app/<id>',methods=['POST','GET'])
@login_required
def approve_apt(id):
    sesdeets=db.session.query(Appointments).get_or_404(id)  
    if session.get('docloggedin')==None :
        return render_template("/users/doclog.html")
    else:
        if sesdeets:       
            ap2_update=Appointments.query.get(id)           

            
            ap2_update.status='1'         
         
    db.session.commit()
    flash("Appointment Will Be Confirmed")
    return redirect('/doctor/dashboard')


@app.route('/doc/diagnosis/<id>',methods=['POST','GET'])
@login_required
def doc_diagnosis_feedback(id):
    sesdeets=db.session.query(Appointments).get_or_404(id)
    docdeets=Appointments.query.filter(Appointments.doctor_id==sesdeets.doctor_id,Appointments.status=='1').all()
    alim=db.session.query(Ailments).all()
    if request.method=='GET':
        return render_template('/users/doctor_diagnosis.html',docdeets=docdeets,sesdeets=sesdeets,alim=alim)
    else:
        if sesdeets !=None:            
            pat=sesdeets.patientdeets.user_id
            docs=sesdeets.doctor_id
            ailment_id=request.form.get('ailment')
            adv=request.form.get('advice')
            date=request.form.get('date')
            pat_ail=PatientAilments(patient_id=pat,ailment_id=ailment_id,advice=adv,doctor_id=docs,diagnosis_date=date)
            db.session.add(pat_ail)
            db.session.commit()
            flash("Information Stored In Database")
            return redirect('/doctor/dashboard')
        else:
            flash("Error While Saving")
            return render_template('/users/bookappointment.html',docdeets=docdeets,sesdeets=sesdeets,alim=alim)
        
@app.route('/doc/patdeets/<id>')
@login_required
def doc_paitentdetails(id):
    pat=db.session.query(Patient).get_or_404(id)
    patsess = Patient.query.filter(Patient.user_id==pat.user_id).first()
    return render_template("/users/doc_patientDetails.html", patsess=patsess)
        
@app.route('/doc/delete_app/<id>', methods=['POST', 'GET'])
@login_required
def delete_apt(id):
    dec = ReasonForm()
    sesdeets = db.session.query(Appointments).get_or_404(id)

    if request.method == 'GET':
        return render_template("/users/decline.html", sesdeets=sesdeets, dec=dec)
    else:
        if dec.validate_on_submit():
            reason = dec.declinereasons.data  # Use dec.declinereason.data to access form field data
            ap2_update = Appointments.query.get(id)
            ap2_update.status = '2'
            ap2_update.Reasons = reason
            db.session.add(ap2_update)
            db.session.commit()
            flash("Appointment Will Be Declined")
            return redirect('/doctor/dashboard')
        else:
            flash("Error Can't Decline")
            return render_template("/users/decline.html", sesdeets=sesdeets, dec=dec)

@app.route('/doc/preg')
@login_required
def all_pregs():
    pregs=db.session.query(Pregnancy).all()
    return render_template("/users/preg.html",pregs=pregs)
        
@app.route('/doctor/dashboard')
@login_required
def doctor_dashboard():
    id=session.get('docloggedin')
    docdeets=db.session.query(Doctor).get_or_404(id)
    return render_template('/users/doctor_dashboard.html',docdeets=docdeets)
        
        
@app.route('/doc/logout')
def doctor_logout():
    if session.get("docloggedin")!= None:
        session.pop("docloggedin",None)
    return redirect('/') 


