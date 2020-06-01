from application import db, login_manager
from flask_login import UserMixin
from application.models import Base
from sqlalchemy.sql import text

# telling flask login that we're representing an account here
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
    role = db.relationship("Role", backref="account", lazy=True)
    orders = db.relationship("Order", backref="account", lazy=True)

    def __repr__(self):
        return f"Account('{self.username}', '{self.email}', '{self.password}')"

    def __init__(self, name):
        self.name = name

    def get_id(self):
        return self.id

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True
    
    @staticmethod
    def has_orders(order_id, user_id):
        statement = text("SELECT * "
                    "FROM account_order, account "
                    "WHERE account_order.account_id = :user "
                    "AND account_order.order_id = :order "
                    "AND account.id = :user;").params(user=user_id, order=order_id)
        res = db.engine.execute(statement)

        response = []
        for row in res:
            response.append({"count": row[0]})

        print(len(response))
        
        return len(response) > 0



class Role(Base):
    name = db.Column(db.String(40), unique=True, nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey("account.id"), nullable=False)

    def __repr__(self):
        return f"User('{self.name}')"
