import sqlalchemy
from sqlalchemy_serializer import SerializerMixin

from src.database.db_session import SqlAlchemyBase


class Lab(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'labs'
    __table_args__ = {'extend_existing': True}

    id          = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name        = sqlalchemy.Column(sqlalchemy.Text)
    description = sqlalchemy.Column(sqlalchemy.Text)
    creator_id  = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))

