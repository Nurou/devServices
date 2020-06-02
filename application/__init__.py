from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, current_user
from application.config import Config_PROD, Config_TEST
from functools import wraps
import os


# database instance preparation
db = SQLAlchemy()

bcrypt = Bcrypt()

# Flask-login configuration
login_manager = LoginManager()
login_manager.login_view = "accounts.login"
login_manager.login_message_category = "info"
login_manager.login_message = "Please login as admin to use this functionality."


def login_required(_func=None, *, role="ANY"):
    def wrapper(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            if not (current_user and current_user.is_authenticated):
                return login_manager.unauthorized()

            acceptable_roles = set(("ANY", *current_user.roles()))

            if role not in acceptable_roles:
                return login_manager.unauthorized()

            return func(*args, **kwargs)

        return decorated_view
        wrapper.__name__ = func.__name__

    return wrapper if _func is None else wrapper(_func)


def create_app(config_test=Config_TEST, config_prod=Config_PROD):
    app = Flask(__name__)

    if os.environ.get("ON_HEROKU"):
        app.debug = False
        app.config.from_object(Config_PROD)

    else:
        app.debug = True
        app.config.from_object(Config_TEST)

    # initialise middleware
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from application.auth.routes import accounts
    from application.orders.routes import orders
    from application.main.routes import main
    from application.errors.handlers import errors

    app.register_blueprint(accounts)
    app.register_blueprint(orders)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    try:
        with app.app_context():
            db.create_all()
    except:
        pass

    return app
