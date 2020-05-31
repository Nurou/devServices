from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from application.config import Config_PROD, Config_TEST


# db object for interacting with the db - can use it to query db
db = SQLAlchemy()
bcrypt = Bcrypt()
# handles the session machinery to help you login and logout users
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.login_message_category = "info"
login_manager.login_message = "Please login to use this functionality."


def create_app(config_test=Config_TEST, config_prod=Config_PROD):
    app = Flask(__name__)

    ENV = "dev"

    if ENV == "dev":
        app.debug = True
        app.config.from_object(Config_TEST)

    else:
        app.debug = False
        app.config.from_object(Config_PROD)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from application.accounts.routes import accounts
    from application.orders.routes import orders
    from application.main.routes import main
    from application.errors.handlers import errors

    app.register_blueprint(accounts)
    app.register_blueprint(orders)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app
