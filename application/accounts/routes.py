
from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from application import db, bcrypt
from application.accounts.forms import (RegistrationForm, LoginForm, UpdateAccountForm, DeleteAccountForm)
from application.accounts.models import Account
accounts = Blueprint('accounts', __name__)


@accounts.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
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
        return redirect(url_for("accounts.login"))
    return render_template("register.html", title="Register", form=form)


@accounts.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("accounts.account"))
    form = LoginForm()
    if request.method == "GET":
        return render_template("login.html", title="Login", form=form)
    if form.validate_on_submit():
        account = Account.query.filter_by(username=form.username.data).first()
        print(account)
        if account and bcrypt.check_password_hash(account.password, form.password.data):
            login_user(account, remember=form.remember.data)
            flash("You have been logged in!", "success")
            return redirect(url_for("accounts.account"))
    flash("Login Unsuccessful. Please check username and password", "danger")
    return redirect(url_for("accounts.login"))


@accounts.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("accounts.login"))


@accounts.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()
    delete_form = DeleteAccountForm()

    if delete_form.delete.data:
        flash("Your account has been deleted.", "danger")
        account = Account.query.get_or_404(current_user.id)
        db.session.delete(account)
        db.session.commit()
        return redirect(url_for("accounts.register"))
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account has been updated!", "success")
        return redirect(url_for("accounts.account"))
    elif request.method == "GET":
        # populate form data
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template(
        "account.html", title="Account", form=form, delete_form=delete_form
    )