from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user
from application import db, bcrypt
from application.auth import login_required

services = Blueprint("services", __name__)


@services.route("/services", methods=["GET"])
@login_required(role="ADMIN")
def view_services():
    return render_template("admin/services.html")
  