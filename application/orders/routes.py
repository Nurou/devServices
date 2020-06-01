from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required
from application import db
from application.orders.models import Order
from application.auth.models import Account
from application.orders.forms import OrderForm

orders = Blueprint("orders", __name__)


# @orders.route("/orders")
# @login_required
# def orders():
#     page = request.args.get("page", 1, type=int)
#     client = Account.query.filter_by(username=username).first_or_404()
#     orders = (
#         Order.query.filter_by(account=client)
#         .order_by(Post.date_posted.desc())
#         .paginate(page=page, per_page=5)
#     )
#     return render_template("orders.html", title="Orders", user=current_user)


@orders.route("/orders/new", methods=["GET", "POST"])
@login_required
def new_order():
    form = OrderForm()
    if form.validate_on_submit():
        order = Order(
            title=form.title.data,
            requirements=form.requirements.data,
            account_id=current_user.id,
        )
        db.session.add(order)
        db.session.commit()
        flash("Your order has been created!", "success")
        return redirect(url_for("orders.user_orders", username=current_user.username))
    return render_template(
        "create_order.html", title="New Orders", form=form, legend="New Order"
    )


@orders.route("/account/<string:username>")
@login_required
def user_orders(username):
    page = request.args.get("page", 1, type=int)
    client = Account.query.filter_by(username=username).first_or_404()
    orders = (
        Order.query.filter_by(account=client)
        .order_by(Order.date_created.desc())
        .paginate(page=page, per_page=5)
    )
    return render_template("user_orders.html", orders=orders, client=client)


@orders.route("/order/<int:order_id>")
@login_required
def order(order_id):
    order = Order.query.get_or_404(order_id)
    print(order)
    return render_template("order.html", title=order.title, order=order)


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
        "create_order.html", title="Update Order", form=form, legend="Update Order"
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
    return redirect(url_for("main.home"))
