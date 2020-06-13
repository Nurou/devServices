from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user
from application import db, bcrypt
from application.auth import login_required
from application.services.forms import AddServiceForm
from application.services.models import Service


services = Blueprint("services", __name__)


@services.route("/admin/services", methods=["GET"])
@login_required(role="ADMIN")
def view_services():
    services = Service.query.all()
    return render_template("admin/services.html", services=services)


@services.route("/admin/services/new", methods=["GET", "POST"])
@login_required
def new_service():
    form = AddServiceForm()
    if form.validate_on_submit():
        service = Service(name=form.name.data,)
        db.session.add(service)
        db.session.commit()
        flash(f"New service {service.name} added!", "success")
        return redirect(url_for("services.view_services"))
    return render_template("admin/create_service.html", form=form, legend="New Service")


@services.route("/admin/service/<int:service_id>/delete", methods=["POST"])
@login_required
def delete_service(service_id):
    service = Service.query.get_or_404(service_id)
    db.session.delete(service)
    db.session.commit()
    flash(f"The service {service.name} has been removed!", "success")
    return redirect(url_for("services.view_services"))
