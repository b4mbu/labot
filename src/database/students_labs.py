import sqlalchemy
from sqlalchemy_serializer import SerializerMixin

from db_session import SqlAlchemyBase


class students_labs(SqlAlchemyBase, SerializerMixin):  # Это класс, описывающий таблицу в бд
    """
    Класс, описывающий схему таблицы в нашей БД.
    students_id          - id студента
    labs_id         - id лабораторной
    variant    - вариант
    """
    __tablename__ = 'students_labs'
    __table_args__ = {'extend_existing': True}

    students_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    labs_id = sqlalchemy.Column(sqlalchemy.Integer)
    variant = sqlalchemy.Column(sqlalchemy.Integer)
