import sqlalchemy
from sqlalchemy_serializer import SerializerMixin

from db_session import SqlAlchemyBase


class UserLab(SqlAlchemyBase, SerializerMixin):
    # TODO Доделать описание
    """
    students_id          - id студента
    labs_id         - id лабораторной
    variant    - вариант
    """
    __tablename__ = 'users_labs'
    __table_args__ = {'extend_existing': True}

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer)
    variant_id = sqlalchemy.Column(sqlalchemy.Integer)
