from application import db
from application.models import Base


class Developer(Base):

    name = db.Column(db.String(100), nullable=False)
    experience_level = db.Column(db.Integer, nullable=True)
    hourly_cost = db.Column(db.Integer, nullable=True)

    def __init__(self, name, experience_level, hourly_cost):
      self.name = name
      self.experience_level = experience_level
      self.hourly_cost = hourly_cost
       
    def __repr__(self):
        return f"Developer('{self.name}', '{self.experience_level}', '{self.hourly_cost}')"
