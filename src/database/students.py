import sqlalchemy
from sqlalchemy_serializer import SerializerMixin

from db_session import SqlAlchemyBase


class students(SqlAlchemyBase, SerializerMixin):  # Это класс, описывающий таблицу в бд
    """
    Класс, описывающий схему таблицы в нашей БД.
    id         - primary key
    fullName   - ФИО студента
    tgUserName - ссылка на тг:  @example
    """
    __tablename__ = 'students'
    __table_args__ = {'extend_existing': True}

    id         = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    fullName   = sqlalchemy.Column(sqlalchemy.Text)
    tgUserName = sqlalchemy.Column(sqlalchemy.Text)

