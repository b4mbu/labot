import sqlalchemy
from sqlalchemy_serializer import SerializerMixin

from src.database.db_session import SqlAlchemyBase


class UserVariant(SqlAlchemyBase, SerializerMixin):
    # TODO Доделать описание
    """
    students_id          - id студента
    labs_id         - id лабораторной
    variant    - вариант
    """
    __tablename__ = 'users_variants'
    __table_args__ = {'extend_existing': True}

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    variant_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("variants.id"))
