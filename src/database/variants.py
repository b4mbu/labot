import sqlalchemy
from sqlalchemy_serializer import SerializerMixin

from src.database.db_session import SqlAlchemyBase


class Variant(SqlAlchemyBase, SerializerMixin):  # Это класс, описывающий таблицу в бд
    # TODO Доделать описание
    """
    Класс, описывающий схему таблицы в нашей БД.
    id           - primary key
    role         - роль пользователя
    full_name    - ФИО пользователя
    tg_user_name - ссылка на тг:  @example
    """
    __tablename__ = 'variants'
    __table_args__ = {'extend_existing': True}

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.Text)
    count = sqlalchemy.Column(sqlalchemy.Integer)
    lab_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("labs.id"))
