from flask import render_template, request, flash, redirect, url_for

# app needs to be imported as it's used by decorators below
from application import app, db, bcrypt
from application.forms import RegistrationForm, LoginForm
from application.models import Account, Role, Order


services = [
    "Mobile",
    "Web",
    "Design",
    "DevOps",
]

developers = [
    {"name": "John Doe", "skills": ["HTML, CSS, JavaScript"],},
    {"name": "Jane Doe", "skills": ["Docker, Kubernetes"],},
]


@app.route("/")
def home():
    return render_template("index.html", services=services, developers=developers)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # hash pw to prepare it for db
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        account = Account(
            username=form.username.data, email=form.email.data, password=hashed_pw
        )
        db.session.add(account)
        db.session.commit()
        flash(
            f"Account created for {form.username.data}! You can now log in", "success"
        )
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
