from flask import Flask, render_template
from flask import session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Import Modules
from forms import LoginForm, SignUpForm
from livereload import Server

import os

app = Flask(__name__)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

#-- SQLAlchemy Database --#
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///authentication.db'
db = SQLAlchemy(app)

class Employee(db.Model):
    employee_id = db.Column(db.Integer, primary_key = True)
    employee_info = db.Column(db.Integer, db.ForeignKey('information.info_id'), nullable = False)
    department_name = db.Column(db.Integer, db.ForeignKey('department.dept_id'), nullable = False)
    # department_head = db.Column(db.Integer, db.ForeignKey('department.dept_id'), nullable = True)

class Information(db.Model):
    info_id = db.Column(db.Integer, primary_key = True, nullable = False)
    first_name = db.Column(db.String(50), nullable = False)
    last_name = db.Column(db.String(50), nullable = False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    employee = db.relationship('Employee', backref = 'info', uselist=False)
    
class Department(db.Model):
    dept_id = db.Column(db.Integer, primary_key = True, nullable = False)
    name = db.Column(db.Integer, unique = True, nullable = False)
    location = db.Column(db.String(120), nullable = False)
    employees = db.relationship('Employee', backref = 'department')
    # head = db.relationship('Employee', backref='head_of_department', uselist=False)

project_members = db.Table('project_members',
    db.Column('employee_id', db.Integer, db.ForeignKey('employee.employee_id'), primary_key=True),
    db.Column('project_id', db.Integer, db.ForeignKey('project.project_id'), primary_key=True)
)

class Project(db.Model):
    project_id = db.Column(db.Integer, primary_key = True, nullable = False)
    name = db.Column(db.String(100), nullable = False)
    members = db.relationship('Employee', secondary=project_members, backref='projects')

db.create_all()
#-- End --#

users = [
    {"id": 1, "full_name": "Pet Rescue Team", "email": "team@pawsrescue.co", "password": "adminpass"},
]

@app.route("/")
def home():
    return render_template("home.html")

# Form need to have defined methods
@app.route("/login", methods=['GET', 'POST'])
def login():

    # Form created with WTForms
    form = LoginForm()

    if form.validate_on_submit():
        user = next((user for user in users if user['email'] == form.email.data and user['password'] == form.password.data), None)
        if user is None:
            return render_template("login.html", form = form, status="alert", message="Incorrect Email or Password")
        else:
            session['user'] = user
            return render_template("login.html", status="confirm", message="Successfully Logged In")
    return render_template("login.html", form = form)

@app.route('/logout')
def logout():
    if 'user' in session:
        session.pop('user')
    return redirect(url_for('home', _scheme='http', _external=True))

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    # Form created with WTForms
    form = SignUpForm()

    depts = Department.query.all()
    print(depts)

    if form.validate_on_submit():
        new_employee = Employee(department_name = form.dept.data, department_head = form.deptHead.data)
        new_employee_info = Information(first_name = form.fName.data, last_name = form.lName.data, email = form.email.data, password = form.password.data)
        db.session.add(new_employee)
        return render_template("signup.html", status="confirm", message="Created account successfully!")

    return render_template("signup.html", form = form, depts = depts)

if __name__ == "__main__":
    server = Server(app.wsgi_app)
    server.watch('templates/')
    server.watch('static/')
    server.serve(port=5000, host='0.0.0.0', debug=True)