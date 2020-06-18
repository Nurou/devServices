from application import db
from application.models import Base
from sqlalchemy.sql import text

class Service(Base):

    name = db.Column(db.String(100), nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"{self.name}"
      
    @staticmethod
    def get_services_by_demand():
        stmt = text(
            " SELECT s.id, s.name, (select count(*) from \"order\" where \"order\".service_id = s.id)  AS total_orders FROM Service s "
            " LEFT JOIN \"order\" ON \"order\".service_id = s.id " 
            " GROUP BY s.id, s.name " 
            " ORDER BY total_orders DESC, s.name " 
        )

        res = db.engine.execute(stmt)

        response = []
        for row in res:
            response.append({"id": row[0], "name": row[1], "orders": row[2]})

        return response
