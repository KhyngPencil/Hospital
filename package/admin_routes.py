import random,string,os
from functools import wraps
from werkzeug.security import generate_password_hash,check_password_hash
from flask import render_template,request,abort,redirect,flash,make_response,session,url_for


#local imports

from package import app,csrf
from package.models import db,Admin,Doctor,Patient,Appointments,Specilaization,Ailments,PatientAilments,Pregnancy
from package.forms import *


def login_required(f):
    @wraps(f)
    def login_check(*args,**kwargs):
        if session.get('adminloggedin')!=None:
            return f(*args,**kwargs)
        else:
            flash("Access Denied,Login To Gain Access")
            return redirect('/admin/login')
    return login_check
@app.after_request
def after_request(response):
    #TO solve teh problem of loggedout user's details being cached in the browser 
    response.headers['Cache-Control']="no-cache, no-store, must-revalidate"
    return response
@app.route('/admin/login/',methods=['POST','GET'])
def adm_login():
    adm=AdminLogForm()
    if request.method =="GET":    
        return render_template("/admin/admi_log.html",adm=adm)
        
    else:
        admin_name=request.form.get('adminame')
        adpwd=request.form.get('adminpwd')
        admins=db.session.query(Admin).filter(Admin.admin_username==admin_name).first()
        if admins!=None:
            hashed_pwd=admins.admin_pwd
            if check_password_hash(hashed_pwd,adpwd)==True:
                session['adminloggedin']=admins.admin_id
                return redirect('/admin/dashboard')
            else:
                flash('Invalid Credentials ')
                return render_template("/admin/admi_log.html",adm=adm)
                #return 'Admin Form Here'
        else:
            flash("Invalid Credentials,Try Again")
            return render_template("/admin/admi_log.html",adm=adm)
            #return 'Admin Form Here'

@app.route('/admin/delete/<id>/')
@login_required
def doctor_delete(id):
    doc=db.session.query(Doctor).get_or_404(id)
    db.session.delete(doc)
    db.session.commit()
    flash('Doctor Data Deleted')
    return redirect(url_for('all_doctors'))

@app.route('/admin/diagnosis')
@login_required
def all_diagnosis():
     dia= db.session.query(PatientAilments).all()
     return render_template("admin/alldiagnoosis.html",dia=dia)
    
    
@app.route('/admin/dashboard')
@login_required
def admin_dash():
    return render_template("admin/admin_dashboard.html")

@app.route('/admin/alldoctors/')
@login_required
def all_doctors():
    doc= db.session.query(Doctor).all()
    return render_template('admin/alldoctors.html',doc=doc)

@app.route('/admin/allpatients/')
@login_required
def all_patients():
    pat= db.session.query(Patient).all()
    return render_template('admin/allappointments.html',pat=pat)

@app.route('/admin/allappointments')
@login_required
def all_appointments():
    apt=db.session.query(Appointments).all()
    return render_template('admin/allpatients.html',apt=apt)

@app.route('/admin/preg/')
@login_required
def pregs():
    pregs=db.session.query(Pregnancy).all()
    return render_template("/admin/allpregs.html",pregs=pregs)

@app.route('/admin/preg/<id>/')
@login_required
def preg_delete(id):
    preg=db.session.query(Pregnancy).get_or_404(id)
    db.session.delete(preg)
    db.session.commit()
    flash('Data Deleted')
    return redirect(url_for('pregs'))

@app.route('/admin/specs')
@login_required
def specialization():
        spec=db.session.query(Specilaization).all()
        return render_template('admin/allspecialization.html',spec=spec)

@app.route('/admin/addspecs',methods=['GET','POST'])
@login_required
def add_specialization():
        spe=SpecForm()
        if request.method=='GET':
            return render_template('admin/regspec.html',spe=spe)
        else:
            if spe.validate_on_submit():
                specname=request.form.get('specname')
                specs=Specilaization(specialization=specname)
                db.session.add(specs)
                db.session.commit()
                flash('Specialization Inserted Into Database')
                return redirect('/admin/specs')
            else:
                flash('Error With Input')
                return render_template('admin/regspec.html',spe=spe)


@app.route('/admin/aliments')
@login_required
def aliments():
        ali=db.session.query(Ailments).all()
        return render_template('admin/allaliments.html',ali=ali)

@app.route('/admin/ali',methods=['GET','POST'])
@login_required
def add_aliments():
        ali=AlimForm()
        if request.method=='GET':
            return render_template('admin/regali.html',ali=ali)
        else:
            if ali.validate_on_submit():
                alimname=request.form.get('alimname')
                alis=Ailments(ailments=alimname)
                db.session.add(alis)
                db.session.commit()
                flash('Specialization Inserted Into Database')
                return redirect('/admin/aliments')
            else:
                flash('Error With Input')
                return render_template('admin/regali.html',ali=ali)         

@app.route('/admin/spec_delete/<id>/')
@login_required
def specialization_delete(id):
    spe=db.session.query(Specilaization).get_or_404(id)
    db.session.delete(spe)
    db.session.commit()
    flash('Specialization Deleted')
    return redirect(url_for('specialization'))



@app.route('/admin/ail_delete/<id>/')
@login_required
def ailments_delete(id):
    ail=db.session.query(Ailments).get_or_404(id)
    db.session.delete(ail)
    db.session.commit()
    flash('Aliments Deleted')
    return redirect(url_for('aliments'))


@app.route('/admin/patient_delete/<id>/')
@login_required
def patient_delete(id):
    pat=db.session.query(Patient).get_or_404(id)
    db.session.delete(pat)
    db.session.commit()
    flash('Patient Data Deleted')
    return redirect(url_for('all_patients'))

@app.route('/admin_logout')
def admin_logout():
    if session.get("adminloggedin") != None:
        session.pop("adminloggedin",None)
    return redirect('/') 