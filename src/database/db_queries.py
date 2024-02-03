from config import config
from src.database import db_session
from src.database.labs           import Lab
from src.database.tokens         import Token
from src.database.users          import User
from src.database.variants       import Variant
from src.database.users_variants import UserVariant
import json
import random
import string


def check_token_role(token_str: str) -> str:
    session = db_session.create_session()
    tokens_result = session.query(Token).filter(Token.token == token_str, Token.count_of_activation > 0).all()
    result = json.dumps({"status": "fail"})

    if tokens_result:
        session.query(Token).filter(
                Token.id == tokens_result[0].id
                ).update({
                    Token.count_of_activation : tokens_result[0].count_of_activation - 1
                })
        session.commit()
        result = json.dumps({
            "status": "ok",
            "role":   tokens_result[0].role,
        })
    session.close()
    return result

def check_user_role(telegram_id: str) -> str:
    session = db_session.create_session()
    user = session.query(User).filter(User.telegram_id == telegram_id).first()
    if user is None:
        session.close()
        return None
    session.close()
    return user.role

def is_exist_user(telegram_id: str) -> bool:
    return check_user_role(telegram_id) is not None

def is_admin(telegram_id: str) -> bool:
    return check_user_role(telegram_id) == "admin"

def is_stud(telegram_id: str) -> bool:
    return check_user_role(telegram_id) == "stud"

def add_new_token(role: str, count_of_activation: int) -> str:
    session = db_session.create_session()

    def rnd_str():
        return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(32))

    token_str = rnd_str() 
    while session.query(Token).filter(Token.token == token_str).all():
        token_str = rnd_str()

    token = Token(token_str, role, count_of_activation)
    session.add(token)
    session.commit()
    session.close()
    return json.dumps({
        "status" : "ok",
        "token"  : token_str,
    })
    
def create_user(full_name: str, role: str, telegram_id: str):
    user = User(role, full_name, telegram_id)
    session = db_session.create_session()
    session.add(user)
    session.commit()
    session.close()
    return json.dumps({"status" : "ok"})

def create_lab(name: str, description: str, creator_telegram_id: str) -> bool:
    session = db_session.create_session()
    user = session.query(User).filter(User.telegram_id == creator_telegram_id and User.role == "admin").first()
    if user is None:
        session.close()
        return False
    lab = Lab(name, description, user.id)
    session.add(lab)
    session.commit()
    session.close()
    return True

def get_all_labs():
    session = db_session.create_session()
    labs = session.query(Lab).all()
    res = "\n\n".join(list([str(lab) for lab in labs]))
    session.close()
    return res

def tmpl():
    session = db_session.create_session()
    session.close()



