from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required
from application import db
from application.orders.models import Order
from application.auth.models import Account
from application.orders.forms import OrderForm, AssignDevsToOrderForm
from application.auth import login_required
from application.services.models import Service
from application.developers.models import Developer

orders = Blueprint("orders", __name__)


def get_service(name):
    print(name)
    print(Service.query.filter_by(name=name).first())
    return Service.query.filter_by(name=name).first().id


@orders.route("/orders/new", methods=["GET", "POST"])
@login_required
def new_order():
    form = OrderForm()
    # services = Service.query.all()
    if form.validate_on_submit():
        print(form.service.data)
        order = Order(
            title=form.title.data,
            requirements=form.requirements.data,
            account_id=current_user.id,
            service_id=form.service.data.id,
            complete=False,
        )
        db.session.add(order)
        db.session.commit()
        flash("Your order has been created!", "success")
        return redirect(url_for("orders.client_orders", username=current_user.username))
    return render_template(
        "client/create_order.html", form=form, legend="New Order", title="New Order"
    )


@orders.route("/account/<string:username>")
@login_required
def client_orders(username):
    page = request.args.get("page", 1, type=int)
    client = Account.query.filter_by(username=username).first_or_404()
    orders = (
        Order.query.filter_by(account=client)
        .order_by(Order.date_created.desc())
        .paginate(page=page, per_page=5)
    )
    return render_template("client/client_orders.html", orders=orders, client=client)


@orders.route("/order/<int:order_id>")
@login_required
def order(order_id):
    order = Order.query.get_or_404(order_id)
    return render_template("client/order.html", title=order.title, order=order)


@orders.route("/order/<int:order_id>/update", methods=["GET", "POST"])
@login_required
def update_order(order_id):
    order = Order.query.get_or_404(order_id)
    if order.account != current_user:
        abort(403)
    form = OrderForm()
    if form.validate_on_submit():
        order.title = form.title.data
        order.requirements = form.requirements.data
        db.session.commit()
        flash("Your order has been updated!", "success")
        return redirect(url_for("orders.order", order_id=order.id))
    elif request.method == "GET":
        form.title.data = order.title
        form.requirements.data = order.requirements
    return render_template(
        "client/create_order.html",
        title="Update Order",
        form=form,
        legend="Update Order",
    )


@orders.route("/order/<int:order_id>/delete", methods=["POST"])
@login_required
def delete_order(order_id):
    order = Order.query.get_or_404(order_id)
    if order.account != current_user:
        abort(403)
    db.session.delete(order)
    db.session.commit()
    flash("Your order has been deleted!", "success")
    return redirect(url_for("orders.client_orders", username=current_user.username))


@orders.route("/admin/agency_orders", methods=["GET"])
@login_required(role="ADMIN")
def agency_orders():
    orders = Order.query.all()
    print(orders)
    for order in orders:
        print(order.account)
    return render_template(
        "admin/agency_orders.html", title="All orders", orders=orders
    )


@orders.route("/admin/order/<int:order_id>", methods=["GET", "POST"])
@login_required(role="ADMIN")
def admin_order(order_id):
    order = Order.query.get_or_404(order_id)
    developers_available = Developer.find_developers_with_skills_and_availability(
        order.service_id
    )
    
    print("**********************************")
    print(developers_available)
    print("**********************************")
    
    form = AssignDevsToOrderForm()

    form.developers.choices = [
        (d.id, d.name)
        for d in Developer.query.all()
        if d.name in developers_available
        # and (Developer.is_developer_already_assigned(order_id, d.id) == True)
    ]
    
    print("**********************************")
    print("AVAILABLE:")
    print(form.developers.choices)
    print("**********************************")
    


    if form.validate_on_submit():
        developer_record = Developer.query.all()
        # need a list to hold our choices
        assigned = []
        # looping through the choices, we check the choice ID against what was passed in the form
        for developer in developer_record:
            # when we find a match, we then append the object to our list
            if developer.id in form.developers.data:
                assigned.append(developer)
        order.developers = assigned
        db.session.add(order)
        db.session.commit()
    return render_template(
        "admin/order.html", title=order.title, order=order, form=form,
    )


@orders.route("/admin/order/<int:order_id>/mark_done", methods=["POST"])
@login_required(role="ADMIN")
def mark_done(order_id):
    order = Order.query.get_or_404(order_id)
    order.complete = True
    db.session.add(order)
    db.session.commit()
    flash("The order was marked as complete.", "success")
    return render_template("admin/order.html", title=order.title, order=order)
