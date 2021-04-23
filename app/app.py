from flask import Flask, render_template, request

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
    # if request.method == "POST":
    #     email = request.form['email']
    #     password = request.form['password']
    #     if email in users and users[email] == password:
    #         return render_template("login.html", message ="Successfully Logged In")
    #     return render_template("login.html", message ="Incorrect Email or Password")
    # return render_template("login.html")

    # Form created with WTForms
    form = LoginForm()

    if form.validate_on_submit():
        for user in users:
            if user['email'] == form.email.data and user['password'] == form.password.data:
                return render_template("login.html", status="confirm", message="Successfully Logged In")
        return render_template("login.html", form = form, status="alert", message="Incorrect Email or Password")
    elif form.errors:
        print(form.errors.items())
        print(form.email.errors)
        print(form.password.errors)
    return render_template("login.html", form = form)

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