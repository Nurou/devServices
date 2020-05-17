from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


# Env config - see SQLAlchemy docs
ENV = "dev"

if ENV == "dev":
    app.debug = True
    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = "postgresql://postgres:123456@localhost/devServices"
else:
    app.debug = False
    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = "postgres://lzhvtfufywmlwi:e28454e9e7ca660b7705a31b201b1dadaddfffa04045034cc353450388d14f69@ec2-18-235-20-228.compute-1.amazonaws.com:5432/d1jvsaumt4o3pl"


# log all queries
app.config["SQLALCHEMY_ECHO"] = True
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "6391c84926554768c34560ab1ff4d839"

# db object for interacting with the db - can use it to query db
db = SQLAlchemy(app)

from application import routes


# creates all the db relations
db.create_all()
