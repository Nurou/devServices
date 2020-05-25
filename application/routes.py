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
from application.forms import (
    RegistrationForm,
    LoginForm,
    UpdateAccountForm,
    DeleteAccountForm,
    OrderForm,
)
from application.models import Account, Role, Order


@app.route("/")
def home():
    return render_template("index.html")


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
            role="client",
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
            return redirect(url_for("account"))
    flash("Login Unsuccessful. Please check username and password", "danger")
    return redirect(url_for("login"))


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()
    delete_form = DeleteAccountForm()

    if delete_form.delete.data:
        flash("Your account has been deleted.", "danger")
        account = Account.query.get_or_404(current_user.id)
        db.session.delete(account)
        db.session.commit()
        return redirect(url_for("register"))
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
    return render_template(
        "account.html", title="Account", form=form, delete_form=delete_form
    )


@app.route("/orders")
@login_required
def orders():
    page = request.args.get("page", 1, type=int)
    client = Account.query.filter_by(username=username).first_or_404()
    orders = (
        Order.query.filter_by(account=client)
        .order_by(Post.date_posted.desc())
        .paginate(page=page, per_page=5)
    )
    return render_template("orders.html", title="Orders", user=current_user)


@app.route("/orders/new", methods=["GET", "POST"])
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
        return redirect(url_for("user_orders", username=current_user.username))
    return render_template(
        "create_order.html", title="New Orders", form=form, legend="New Order"
    )


@app.route("/account/<string:username>")
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


@app.route("/order/<int:order_id>")
@login_required
def order(order_id):
    order = Order.query.get_or_404(order_id)
    print(order)
    return render_template("order.html", title=order.title, order=order)


@app.route("/order/<int:order_id>/update", methods=["GET", "POST"])
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
        return redirect(url_for("order", order_id=order.id))
    elif request.method == "GET":
        form.title.data = order.title
        form.requirements.data = order.requirements
    return render_template(
        "create_order.html", title="Update Order", form=form, legend="Update Order"
    )


@app.route("/order/<int:order_id>/delete", methods=["POST"])
@login_required
def delete_order(order_id):
    order = Order.query.get_or_404(order_id)
    if order.account != current_user:
        abort(403)
    db.session.delete(order)
    db.session.commit()
    flash("Your order has been deleted!", "success")
    return redirect(url_for("home"))
