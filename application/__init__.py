from flask import Flask
app = Flask(__name__)

from flask_sqlalchemy import SQLAlchemy

# Env config - see SQLAlchemy docs
ENV = 'dev'

if ENV == 'dev':
  app.debug = True
  app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:123456@localhost/devServices"
else:
  app.debug = False
  app.config["SQLALCHEMY_DATABASE_URI"] = ""

# # configure database URI
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///services.db"

# log all queries
app.config["SQLALCHEMY_ECHO"] = True

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# db object for interacting with the db - can use it to query db
db = SQLAlchemy(app)

from application import views

from application.services import models

# creates all the db relations
db.create_all()