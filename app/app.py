from flask import Flask, render_template
from flask import session, redirect, url_for

# Import Modules
from forms import LoginForm, SignUpForm
from livereload import Server

import os

app = Flask(__name__)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

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

    if form.validate_on_submit():
        new_user = {"id": len(users)+1, "full_name": form.fName.data, "email": form.email.data, "password": form.password.data}
        print(new_user['email'])
        for user in users:
            if user['email'] == new_user['email']:
                return render_template("signup.html", form = form, status="alert", message="Existed User!")
        return render_template("signup.html", status="confirm", message="Created account successfully!")

    return render_template("signup.html", form = form)

if __name__ == "__main__":
    server = Server(app.wsgi_app)
    server.watch('templates/')
    server.watch('static/')
    server.serve(port=5000, host='0.0.0.0', debug=True)