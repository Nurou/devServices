from flask import render_template, request, flash, redirect, url_for
from flask_login import (
    login_user,
    logout_user,
    current_user,
    logout_user,
    login_required,
)

# app needs to be imported as it's used by decorators below
from application import app, db, bcrypt
from application.forms import RegistrationForm, LoginForm, UpdateAccountForm
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
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        # hash pw to prepare it for db
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        account = Account(
            name=form.name.data,
            email=form.email.data,
            username=form.username.data,
            password=hashed_pw,
        )
        db.session.add(account)
        db.session.commit()
        flash(
            f"Account created for {form.username.data}! You can now log in", "success"
        )
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if request.method == "GET":
        return render_template("login.html", title="Login", form=form)
    if form.validate_on_submit():
        account = Account.query.filter_by(username=form.username.data).first()
        print(account)
        if account and bcrypt.check_password_hash(account.password, form.password.data):
            login_user(account, remember=form.remember.data)
            flash("You have been logged in!", "success")
            return redirect(url_for("home"))
    flash("Login Unsuccessful. Please check username and password", "danger")
    return redirect(url_for("login"))


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account has been updated!", "success")
        return redirect(url_for("account"))
    elif request.method == "GET":
        # populate form data
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template("account.html", title="Account", form=form)
