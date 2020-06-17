from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user
from application import db, bcrypt
from application.auth import login_required
from application.orders.models import Order
from application.developers.forms import AddDeveloperForm
from application.developers.models import Developer
from application.services.models import Service

developers = Blueprint("developers", __name__)


@developers.route("/admin/developers", methods=["GET"])
@login_required(role="ADMIN")
def view_developers():
    developers = Developer.query.all()
    return render_template("admin/developers.html", developers=developers)


@developers.route("/admin/developers/new", methods=["GET", "POST"])
@login_required
def new_developer():
    form = AddDeveloperForm()

    form.services.choices = [(s.id, s.name) for s in Service.query.all()]

    if form.validate_on_submit():
        service_record = Service.query.all()
        # need a list to hold our choices
        selected = []
        # looping through the choices, we check the choice ID against what was passed in the form
        for service in service_record:
            # when we find a match, we then append the object to our list
            if service.id in form.services.data:
                selected.append(service)
        developer = Developer(
            name=form.name.data,
            experience_level=form.experience_level.data,
            hourly_cost=form.hourly_cost.data,
        )
        developer.services = selected
        db.session.add(developer)
        db.session.commit()
        flash(f"Developer {developer.name} has been added", "success")
        return redirect(url_for("developers.view_developers"))

    return render_template(
        "/admin/add_developer.html", form=form, legend="New Developer",
    )


@developers.route("/admin/developers/assign/<int:order_id>", methods=["GET"])
@login_required(role="ADMIN")
def assign_developer(order_id):
    order = Order.query.get_or_404(order_id)
    return render_template("admin/developers.html")
