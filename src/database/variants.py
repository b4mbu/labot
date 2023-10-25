import sqlalchemy
from sqlalchemy_serializer import SerializerMixin

from db_session import SqlAlchemyBase


class variants(SqlAlchemyBase, SerializerMixin):  # Это класс, описывающий таблицу в бд
    """
    Класс, описывающий схему таблицы в нашей БД.
    id           - primary key
    role         - роль пользователя
    full_name    - ФИО пользователя
    tg_user_name - ссылка на тг:  @example
    """
    __tablename__ = 'labs'
    __table_args__ = {'extend_existing': True}

    id         = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name       = sqlalchemy.Column(sqlalchemy.Text)
    description   = sqlalchemy.Column(sqlalchemy.Text)
    creators_id = sqlalchemy.Column(sqlalchemy.Text)


