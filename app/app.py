from flask import Flask, render_template, request

# Import Modules
from forms import LoginForm
from livereload import Server

import os

app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

users = {
    "archie.andrews@email.com": "football4life",
    "veronica.lodge@email.com": "fashiondiva"
}

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
        for u_email, u_password in users.items():
            if u_email == form.email.data and u_password == form.password.data:
                return render_template("login.html", message ="Successfully Logged I=n")
        return render_template("login.html", form = form, message ="Incorrect Email or Password")
    elif form.errors:
        print(form.errors.items())
        print(form.email.errors)
        print(form.password.errors)
    return render_template("login.html", form = form)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)