from application import db
from application.models import Base


class Order(Base):
    title = db.Column(db.String(100), nullable=False)
    requirements = db.Column(db.Text)
    account_id = db.Column(db.Integer, db.ForeignKey("account.id"), nullable=False)

    def __repr__(self):
        return f"User('{self.title}', '{self.requirements}', '{self.date_created}', '{self.date_modified}')"
