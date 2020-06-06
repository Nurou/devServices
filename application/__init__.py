from flask_sqlalchemy import SQLAlchemy
from flask import Flask
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
          from application.auth.models import Role, Account
          from application.orders.models import Order  
          db.create_all()
    except:
        pass

    try:
        with app.app_context():
            from application.auth.models import Role, Account
            from application.orders.models import Order
            
            role = Role.query.filter_by(name='ADMIN').first()
            if not role:
              role = Role('ADMIN')
              db.session().add(role)
              db.session().commit()
            role = Role.query.filter_by(name='CLIENT').first()
            if not role:
              role = Role('CLIENT')
              db.session().add(role)
              db.session().commit()
    except:
        pass

    return app
