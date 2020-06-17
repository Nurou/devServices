from application import db
from application.models import Base
from sqlalchemy.sql import text

# maximum number of orders a developer can be working on at any given time
max_orders = 4

developer_skills = db.Table(
    "developer_skills",
    Base.metadata,
    db.Column("developer_id", db.Integer, db.ForeignKey("developer.id")),
    db.Column("service_id", db.Integer, db.ForeignKey("service.id")),
)


class Developer(Base):

    name = db.Column(db.String(100), nullable=False)
    experience_level = db.Column(db.Integer, nullable=True)
    hourly_cost = db.Column(db.Integer, nullable=True)
    # many-to-many rel to services
    services = db.relationship(
        "Service", secondary=developer_skills, backref="developers", lazy="dynamic"
    )

    def __init__(self, name, experience_level, hourly_cost):
        self.name = name
        self.experience_level = experience_level
        self.hourly_cost = hourly_cost

    def __repr__(self):
        return (
            f"Developer('{self.name}', '{self.experience_level}', '{self.hourly_cost}')"
        )

    @staticmethod
    def find_developers_with_skills_and_availability(service_id):
        stmt = text(
            "SELECT d.name "
            "FROM developer d "
            "LEFT JOIN developer_skills ds ON d.id = ds.developer_id "
            "WHERE service_id = :service_id AND (SELECT count(order_id) FROM order_developers) < :max_orders "
            "GROUP BY d.name"
        ).params(service_id=service_id, max_orders=max_orders)
        res = db.engine.execute(stmt)

        response = []
        for row in res:
            response.append(row[0])

        return response

    @staticmethod
    def is_developer_available(developer_id):
        stmt = text(
            "SELECT count(order_id) FROM order_developers "
            "WHERE developer_id = :developer_id "
        ).params(developer_id=developer_id)
        res = db.engine.execute(stmt)

        print(res)
        if res < max_orders:
            return True
        return False

    @staticmethod
    def is_developer_already_assigned(order_id, developer_id):
        stmt = text(
            "SELECT order_id, developer_id FROM order_developers "
            "WHERE developer_id = :developer_id AND order_id = :order_id "
        ).params(developer_id=developer_id, order_id=order_id)
        res = db.engine.execute(stmt)

        if not res:
            return False

        return True
