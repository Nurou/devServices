from flask import render_template, request, flash, redirect, url_for

# app needs to be imported as it's used by decorators below
from application import app
from application.forms import RegistrationForm, LoginForm


services = [
    "Mobile",
    "Web",
    "Design",
    "DevOps",
]

developers = [
    {"name": "John Doe", "skills": ["html, css, JavaScript"],},
    {"name": "Jane Doe", "skills": ["Docker, Node, CI"],},
]


@app.route("/")
def home():
    return render_template("index.html", services=services, developers=developers)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f"Account created for {form.username.data}!", "success")
        return redirect(url_for("home"))
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == "admin@agency.com" and form.password.data == "password":
            flash("You have been logged in!", "success")
            return redirect(url_for("home"))
        else:
            flash("Login Unsuccessful. Please check username and password", "danger")
    return render_template("login.html", title="Login", form=form)


@app.route("/submit", methods=["POST"])
def submit():
    if request.method == "POST":
        client_name = request.form["client-name"]
        client_phone_number = request.form["client-phone-number"]
        """ TODO: rest of form data """
        print(client_name)
        print(client_phone_number)
        if client_name == "" or client_phone_number == "":
            return render_template("index.html", message="Please enter required fields")
    return render_template("success.html")
