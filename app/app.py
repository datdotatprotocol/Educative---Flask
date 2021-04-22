from flask import Flask, render_template, request
from flask_wtf import FlaskForm

# Import Modules
from forms import LoginForm

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

    if form.is_submitted():
        print('Submitted.')
    
    if form.validate():
        print('Valid.')

    if form.validate_on_submit():
        print('Submitted and Valid.')

    return render_template("login.html", form = form)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)