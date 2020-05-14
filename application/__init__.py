from flask import Flask
app = Flask(__name__)

from flask_sqlalchemy import SQLAlchemy

# configure database URI
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///services.db"

# log all queries
app.config["SQLALCHEMY_ECHO"] = True

# db object for interacting with the db
db = SQLAlchemy(app)

from application import views

from application.services import models

# creates all the db relations
db.create_all()