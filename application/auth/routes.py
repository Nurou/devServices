
from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user
from application import db, bcrypt
from application.auth import login_required
from application.auth.forms import (RegistrationForm, LoginForm, UpdateAccountForm, DeleteAccountForm)
from application.auth.models import Account, Role
from sqlalchemy.sql import text

accounts = Blueprint('accounts', __name__)

@accounts.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        # hash pw to prepare it for db
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        role = Role.query.filter_by(name='CLIENT').first()
        print(f"role: {role}")
        account = Account(
            name=form.name.data,
            email=form.email.data,  
            username=form.username.data,
            password=hashed_pw,
            role=role
        )
        db.session.add(account)
        db.session.commit()
        flash(
            f"Account created for {form.username.data}! You can now log in", "success"
        )
        return redirect(url_for("accounts.login"))
    return render_template("client/register.html", title="Register", form=form)


@accounts.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("accounts.account"))
    form = LoginForm()
    if request.method == "GET":
        return render_template("client/login.html", title="Login", form=form)
    if form.validate_on_submit():
        account = Account.query.filter_by(username=form.username.data).first()
        print(account)
        if account and bcrypt.check_password_hash(account.password, form.password.data):
            login_user(account, remember=form.remember.data)
            flash("You have been logged in!", "success")
            if(account.role.name == 'ADMIN'):
              return redirect(url_for("accounts.dashboard"))
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
        form.username.data = current_user.username
        form.email.data = current_user.email
    
    
    return render_template(
        "client/account.html", title="Account", form=form, delete_form=delete_form, name=current_user.username
    )
    
@accounts.route("/admin_credentials", methods=["GET"])
def admin_credentials():
    return render_template(
        "client/admin.html", title="Admin Credentials"
    )
    
@accounts.route("/admin", methods=["GET"])
@login_required(role="ADMIN")
def admin_home():
    return redirect(url_for("accounts.dashboard"))
    
@accounts.route("/admin/dashboard", methods=["GET"])
@login_required(role="ADMIN")
def dashboard():
    return render_template(
        "admin/dashboard.html", title="Admin Dashboard"
    )
    
@accounts.route("/admin/clients", methods=["GET"])
@login_required(role="ADMIN")
def clients():
    return render_template(
        "admin/clients.html", title="Clients", no_orders=Account.find_clients_with_no_orders(), with_orders=Account.find_clients_and_orders()
    )
    
  