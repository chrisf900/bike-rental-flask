from uuid import UUID

import bcrypt
from dotenv import load_dotenv
from flask_jwt_extended import get_jti

from database import RedisClient
from users import providers, services
from users.lib.exceptions import UserNotFoundError

load_dotenv(".env")


def get_user_pw(user_uuid: UUID | str) -> str:
    return providers.get_user_pw(user_uuid)


def get_password_hash(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode()


def verify_password(non_hashed_pass, hashed_pass) -> bool:
    return bcrypt.checkpw(non_hashed_pass.encode(), hashed_pass.encode())


def authenticate_user(username: str, password: str):
    user = services.get_user_by_email(user_email=username)
    user_pw = get_user_pw(user_uuid=user.uuid)

    if not verify_password(password, user_pw):
        raise UserNotFoundError
    return user


def check_if_token_is_revoked(encoded_token):
    redis_client = RedisClient()

    jti = get_jti(encoded_token=encoded_token)
    token_in_redis = redis_client.conn.get(name=jti)
    return token_in_redis is not None
