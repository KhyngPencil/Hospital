from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,TextAreaField,PasswordField,SubmitField,DateField,IntegerField,FileField,RadioField
from wtforms.validators import Email,DataRequired,EqualTo,Length

class RegForm(FlaskForm):
    fname= StringField("FirstName",validators=[DataRequired()])
    lname= StringField("LastName",validators=[DataRequired(),Length(min=5)])
    usermail= StringField("Email",validators=[Email(),DataRequired(message='MY Guy Put Email Naaaa....')])
    pwd= PasswordField("Enter Password",validators=[DataRequired()])
    confpwd= PasswordField("Confirm Password",validators=[EqualTo('pwd')])
    username= StringField("Username",validators=[DataRequired(message='Please Input A Username')])
    phone= StringField("Phone Number",validators=[DataRequired(),Length(min=11)])
    address= StringField("Home Address",validators=[DataRequired()])
    profile= TextAreaField("Your Profile",validators=[DataRequired()])
    btnsubmit=SubmitField("Register!")
    department=StringField("Your Department",validators=[DataRequired(message='Please Specify Your Department')])

class LogForm(FlaskForm):
    username= StringField("Username",validators=[DataRequired(message='Please Input The Correct Username')])
    pwd=PasswordField("Password",validators=[DataRequired(message='Incorrect Password Try Again Later')])
    btnlogin=SubmitField('Login')

class DocLogForm(FlaskForm):
    docemail= StringField('Email',validators=[DataRequired(message='Please Input A Correct Username')])
    docpwd= PasswordField('Password',validators=[DataRequired(message='Incorrect Password Try Again Later')])
    docbtnlogin=SubmitField('Login')

class SpecForm(FlaskForm):
    specname= StringField('Specialization',validators=[DataRequired(message='Please Input A Specialization Name')])    
    specbtnsubmit=SubmitField('Add')

class AlimForm(FlaskForm):
    alimname= StringField('Aliment',validators=[DataRequired(message='Please Input A Correct Aliment Name')])    
    alimbtnsubmit=SubmitField('Add')
class ReasonForm(FlaskForm):
    declinereasons= StringField('Reasons For Declining',validators=[DataRequired(message='Please Input A Reason')])    
    decbtnsubmit=SubmitField('Submit')

class PregForm(FlaskForm):
    edd = DateField("Expected Date Of Delivery")
    pregbtn=SubmitField('Submit')



class AdminLogForm(FlaskForm):
    adminame= StringField('Username',validators=[DataRequired(message='Please Input A Correct Username')])
    adminpwd= PasswordField('Password',validators=[DataRequired(message='Incorrect Password Try Again Later')])
    adminbtnlogin=SubmitField('Login')

class CreateAccount(FlaskForm):
    fname = StringField('First name',validators=[DataRequired(message="First name must not be empty")])
    lname = StringField('Last name',validators=[DataRequired(message="Last Name Cannot Be Empty")])
    phn = StringField('Phone Number',validators=[DataRequired(message="Phone Number Cannot Be Empty")])
    Dob = DateField("Date of birth")
    pwd = PasswordField("Password",validators=[DataRequired(message="Password Field Cannot be empty")])
    cpwd = PasswordField("Confirm Password",validators=[EqualTo("pwd",message="Confirm Password Does Not Match"),DataRequired(message="Cannot be empty")])
    email = StringField("Email",validators=[Email(message="invalid email"),DataRequired(message="Emmail Cannot be empty")])
    subbtn = SubmitField("Submit")   
    photo = FileField("Profile Picture")
    gender = RadioField("Gender",choices=[("Male","Male"),("Female","Female")])
    pregstatus= RadioField(choices=[("1","Yes"),("0","No")])
    EDD = DateField("Expected Date Of Delivery")
    address = StringField('Home Address',validators=[DataRequired(message="Home address must be inputed")])
    username=StringField('Username',validators=[DataRequired(message="Username must not be empty")])
    mStatus = RadioField("Gender",choices=[("Single","Single"),("Married","Married"),("Divorced","Divorced")])