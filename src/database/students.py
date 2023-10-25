import sqlalchemy
from sqlalchemy_serializer import SerializerMixin

from db_session import SqlAlchemyBase


class students(SqlAlchemyBase, SerializerMixin):  # Это класс, описывающий таблицу в бд
    """
    Класс, описывающий схему таблицы в нашей БД.
    id           - primary key
    role         - роль пользователя
    full_name    - ФИО пользователя
    tg_user_name - ссылка на тг:  @example
    """
    __tablename__ = 'students'
    __table_args__ = {'extend_existing': True}

    id           = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    role         = sqlalchemy.Column(sqlalchemy.Text)
    full_name    = sqlalchemy.Column(sqlalchemy.Text)
    tg_user_name = sqlalchemy.Column(sqlalchemy.Text)
    password     = sqlalchemy.Column(sqlalchemy.Text)

