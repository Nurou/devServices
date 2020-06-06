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

          acceptable_roles = set(("ANY", *current_user.roles()))
          
          print(current_user.id)
          print(acceptable_roles)
          
          if role not in acceptable_roles:
              return login_manager.unauthorized()

          return func(*args, **kwargs)

      return decorated_view
      wrapper.__name__ = func.__name__

  return wrapper if _func is None else wrapper(_func)
  
  
# Define the UserRoles association table
class AccountRoles(db.Model):
    __tablename__ = 'account_roles'
    id = db.Column(db.Integer(), primary_key=True)
    account_id = db.Column(db.Integer(), db.ForeignKey('account.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('role.id', ondelete='CASCADE'))


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
    roles = db.relationship("Role", backref="account", lazy=True, secondary='account_roles', uselist=False)
    orders = db.relationship("Order", backref="account", lazy=True)

    def __repr__(self):
        return f"Account('{self.name}','{self.username}', '{self.email}', '{self.password}')"

    def __init__(self, name, username, password, email, roles):
        self.name = name
        self.username = username
        self.password = password
        self.email = email
        self.roles = roles

    def roles(self):
        print("*********")
        account=Account.query.filter_by(username=self.username).first()
        roles = Role.query.filter_by(account_id=account.id)
        print(account)
        print("*********")
        return ["ADMIN"]


class Role(Base):  
    name = db.Column(db.String(40), unique=True, nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"User('{self.name}')"
