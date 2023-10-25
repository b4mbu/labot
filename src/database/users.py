import sqlalchemy
from sqlalchemy_serializer import SerializerMixin

from src.database.db_session import SqlAlchemyBase


class User(SqlAlchemyBase, SerializerMixin):
    # TODO Доделать описание
    """
    id           - primary key
    role         - роль пользователя
    full_name    - ФИО пользователя
    tg_username - ссылка на тг:  @example
    """
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    role = sqlalchemy.Column(sqlalchemy.Text)
    full_name = sqlalchemy.Column(sqlalchemy.Text)
    telegram_id = sqlalchemy.Column(sqlalchemy.Integer)
