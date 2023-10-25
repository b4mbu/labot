from src.database import db_session
db_session.global_init()

sessions = db_session.create_session()

sessions.close()