import sqlalchemy
from sqlalchemy_serializer import SerializerMixin

from db_session import SqlAlchemyBase


class Token(SqlAlchemyBase, SerializerMixin):
    # TODO Доделать описание
    """
    students_id          - id студента
    labs_id         - id лабораторной
    variant    - вариант
    """
    __tablename__ = 'tokens'
    __table_args__ = {'extend_existing': True}

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    token = sqlalchemy.Column(sqlalchemy.Text)
    role = sqlalchemy.Column(sqlalchemy.Text)
    count_of_activation = sqlalchemy.Column(sqlalchemy.Integer)