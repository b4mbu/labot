import sqlalchemy
from sqlalchemy_serializer import SerializerMixin

from db_session import SqlAlchemyBase


class Password(SqlAlchemyBase, SerializerMixin):
    # TODO Доделать описание
    """
    students_id          - id студента
    labs_id         - id лабораторной
    variant    - вариант
    """
    __tablename__ = 'passwords'
    __table_args__ = {'extend_existing': True}

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    password = sqlalchemy.Column(sqlalchemy.Integer)
    role = sqlalchemy.Column(sqlalchemy.Text)
