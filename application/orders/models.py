from application import db
from application.models import Base


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(100), nullable=False)
    requirements = db.Column(db.Text)
    account_id = db.Column(db.Integer, db.ForeignKey("account.id"), nullable=False)
    
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
    )
    
    def __init__(self, title, requirements, account_id):
      self.title = title
      self.requirements = requirements
      self.account_id = account_id
       
    def __repr__(self):
        return f"User('{self.title}', '{self.requirements}', '{self.date_created}', '{self.date_modified}')"
