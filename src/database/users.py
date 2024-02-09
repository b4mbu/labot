import sqlalchemy
from sqlalchemy_serializer import SerializerMixin

from src.database.db_session import SqlAlchemyBase


class User(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    role = sqlalchemy.Column(sqlalchemy.Text)
    full_name = sqlalchemy.Column(sqlalchemy.Text)
    telegram_id = sqlalchemy.Column(sqlalchemy.BigInteger)

    def __init__(self, role: str, full_name: str, telegram_id: int):
        self.role = role
        self.full_name = full_name
        self.telegram_id = telegram_id

    def __str__(self):
        return f"role={self.role}, name={self.full_name}, tg_id={self.telegram_id}"
