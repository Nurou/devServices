from flask import Flask
app = Flask(__name__)

from flask_sqlalchemy import SQLAlchemy

# Env config - see SQLAlchemy docs
ENV = 'prod'

if ENV == 'dev':
  app.debug = True
  app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:123456@localhost/devServices"
else:
  app.debug = False
  app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://lzhvtfufywmlwi:e28454e9e7ca660b7705a31b201b1dadaddfffa04045034cc353450388d14f69@ec2-18-235-20-228.compute-1.amazonaws.com:5432/d1jvsaumt4o3pl"

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