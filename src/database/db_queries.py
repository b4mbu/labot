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
        "token"  : token,
        })
    

def create_user(user_data: str):
    user_data = json.loads(user_data)
    user = User(user_data["role"], user_data["full_name"], user_data["telegram_id"])
    session = db_session.create_session()
    session.add(User)
    session.commit()
    session.close()
    return json.dumps({"status" : "ok"})











def tmpl():
    session = db_session.create_session()
    session.close()



