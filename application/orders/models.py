from application import db
from application.models import Base


assigned_developers = db.Table('order_developers', Base.metadata, db.Column('order_id', db.Integer, db.ForeignKey('order.id')),
    db.Column('developer_id', db.Integer, db.ForeignKey('developer.id')))

class Order(Base):
    title = db.Column(db.String(100), nullable=False)
    requirements = db.Column(db.Text)
    complete = db.Column(db.Boolean, default=False, nullable=True)
    account_id = db.Column(db.Integer, db.ForeignKey("account.id"), nullable=True)
    #many-to-one rel to services
    service = db.relationship("Service", backref="order", lazy=True)
    service_id = db.Column(db.Integer, db.ForeignKey("service.id"), nullable=True)
    #many-to-many rel to developers
    developers = db.relationship('Developer',
                    secondary=assigned_developers, backref='orders', lazy='dynamic')

    def __init__(self, title, requirements, account_id):
      self.title = title
      self.requirements = requirements
      self.account_id = account_id
       
    def __repr__(self):
        return f"Order('{self.title}', '{self.requirements}', '{self.date_created}', '{self.date_modified}')"
