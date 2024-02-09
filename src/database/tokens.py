import sqlalchemy
from sqlalchemy_serializer import SerializerMixin

from src.database.db_session import SqlAlchemyBase


class Token(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "tokens"
    __table_args__ = {"extend_existing": True}

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    token = sqlalchemy.Column(sqlalchemy.Text)
    role = sqlalchemy.Column(sqlalchemy.Text)
    count_of_activation = sqlalchemy.Column(sqlalchemy.Integer)

    def __init__(self, token_str: str, role: str, count_of_activation: int):
        self.token = token_str
        self.role = role
        self.count_of_activation = count_of_activation

    def __str__(self):
        return f"role={self.role}, cnt={self.count_of_activation}, token={self.token}"
