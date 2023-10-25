from pydantic import config
import sqlalchemy as sa
import sqlalchemy.ext.declarative as dec
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
from config import config

SqlAlchemyBase = dec.declarative_base()

__factory = None


def global_init(config : config.DatabaseConfig):
    global __factory

    if __factory:
        return

    conn_str = f'postgresql://{config.username}:{config.password}@{config.host}:{config.port}/{config.db_name}'
    print(f'Connected to database {conn_str}')

    engine = sa.create_engine(conn_str)
    __factory = orm.sessionmaker(bind=engine)

    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    global __factory
    return __factory()
