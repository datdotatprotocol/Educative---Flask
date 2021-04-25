from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import InputRequired, Email, EqualTo

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Login ')

class SignUpForm(FlaskForm):
    fName = StringField('Full Name', validators=[InputRequired()])
    lName = StringField('Last Name', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired(), EqualTo('passwordCf')])
    passwordCf = PasswordField('Confirm Password', validators=[InputRequired()])
    dept = SelectField('What is your dept?', choices=[('da', 'Data Analyst'), ('mkt', 'Marketing'), ('tech', 'Technology')])
    deptHead = SelectField('Are you dept head?', choices=[('n', 'No'), ('y', 'Yes')])
    submit = SubmitField('SignUp')