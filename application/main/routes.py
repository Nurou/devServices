
from flask import render_template, request, redirect, url_for, Blueprint
from flask_login import current_user

main = Blueprint('main', __name__)

@main.route("/")
def home():
    if current_user.is_authenticated:
        if current_user.role.name == 'ADMIN':
          return redirect(url_for("accounts.dashboard"))
        return redirect(url_for("accounts.account"))
    return render_template("index.html")