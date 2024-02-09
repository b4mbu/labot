import sqlalchemy
from sqlalchemy_serializer import SerializerMixin

from src.database.db_session import SqlAlchemyBase


class Variant(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "variants"
    __table_args__ = {"extend_existing": True}

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.Text)
    task = sqlalchemy.Column(sqlalchemy.Text)
    count = sqlalchemy.Column(sqlalchemy.Integer)
    lab_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("labs.id"))

    def __init__(self, name: str, task: str, count: int, lab_id: int):
        self.name = name
        self.task = task
        self.count = count
        self.lab_id = lab_id

    def __str__(self):
        return f"name={self.name}, task={self.task}, left={self.count}"

