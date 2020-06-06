from application import db, login_manager
from flask_login import UserMixin
from application.models import Base
from sqlalchemy.sql import text

from application import current_user
from functools import wraps

# telling flask login that we're representing an account here
# this callback is used to reload the user object from the user ID stored in the session
@login_manager.user_loader
def load_user(account_id):
    return Account.query.get(int(account_id))
  
  
def login_required(_func=None, *, role="ANY"):
  def wrapper(func):
      @wraps(func)
      def decorated_view(*args, **kwargs):
          if not (current_user and current_user.is_authenticated):
              return login_manager.unauthorized()

          unauthorized = False

          if role != "ANY":
              unauthorized = True
              
              user_role = current_user.role.name
              
              if user_role == role:
                  unauthorized = False
                  
          if unauthorized:
              return login_manager.unauthorized()

          return func(*args, **kwargs)

      return decorated_view
      wrapper.__name__ = func.__name__

  return wrapper if _func is None else wrapper(_func)
  


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
    role = db.relationship("Role", backref="account", lazy=True)
    role_id = db.Column(db.Integer, db.ForeignKey("role.id"), nullable=True)
    orders = db.relationship("Order", backref="account", lazy=True)

    def __repr__(self):
        return f"Account('{self.name}','{self.username}', '{self.email}', '{self.password}', '{self.role}')"

    def __init__(self, name, username, password, email, role):
        self.name = name
        self.username = username
        self.password = password
        self.email = email
        self.role = role

    def roles(self):
        account=Account.query.filter_by(username=self.username).first()
        return account.role.name


class Role(Base):  
    name = db.Column(db.String(40), unique=True, nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Role('{self.name}')"
