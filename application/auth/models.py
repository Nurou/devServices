from application import db, login_manager
from flask_login import UserMixin
from application.models import Base
from sqlalchemy.sql import text

# telling flask login that we're representing an account here
# this callback is used to reload the user object from the user ID stored in the session
@login_manager.user_loader
def load_user(account_id):
    return Account.query.get(int(account_id))


# user mixin adds the properties that belong to it to our model class
# includes is_active, is_authenticated ...
class Account(Base, UserMixin):
    name = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    """ Role: will get all roles for this account - referencing the 'Role' class
        backref: the account can be referenced from Role by the backref 
        lazy=True - db will load data in one go as necessary
     """
    roles = db.relationship("Role", backref="account", lazy=True)
    orders = db.relationship("Order", backref="account", lazy=True)

    def __repr__(self):
        return f"Account('{self.username}', '{self.email}', '{self.password}')"

    def __init__(self, name):
        self.name = name

    def roles(self):
        return ["ADMIN"]


class Role(Base):
    name = db.Column(db.String(40), unique=True, nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey("account.id"), nullable=False)

    def __repr__(self):
        return f"User('{self.name}')"
