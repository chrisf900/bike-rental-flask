from datetime import datetime
from uuid import UUID

from sqlalchemy.exc import IntegrityError

from database import db
from users.lib.exceptions import (
    EmailAlreadyRegisteredError,
    ProfileAlreadyExistsError,
    UserNotFoundError,
)
from users.models import Gender, PasswordHistory, User


def get_user_by_external_id(user_external_id: int) -> User:
    user = db.session.query(User).filter_by(external_id=user_external_id).scalar()
    if not user:
        raise UserNotFoundError()
    return user


def get_user_by_email(user_email: str) -> User:
    user = db.session.query(User).filter_by(email=user_email).scalar()
    if not user:
        raise UserNotFoundError()
    return user


def get_user_pw(user_uuid: UUID | str) -> PasswordHistory:
    user_data = (
        db.session.query(PasswordHistory).filter_by(user_uuid=user_uuid).scalar()
    )
    if not user_data:
        raise UserNotFoundError()
    return user_data.password


def get_gender_by_name(name: str) -> Gender:
    return db.session.query(Gender).filter_by(name=name.capitalize()).scalar()


def create_profile(
    first_name: str,
    last_name: str,
    gender_id: str,
    birthday: str,
    country_code: str,
    email: str,
    phone_number: int,
    password: str,
) -> User:
    try:
        user = User(
            first_name=first_name,
            last_name=last_name,
            gender_id=gender_id,
            birthday=birthday,
            country_code=country_code,
            email=email,
            phone_number=phone_number,
        )
        db.session.add(user)
        db.session.flush()

        password_history = PasswordHistory(user_uuid=user.uuid, password=password)
        db.session.add(password_history)

        db.session.commit()
    except IntegrityError:
        raise ProfileAlreadyExistsError()

    return user


def update_user_contact_info(
    user_external_id: int, email: str = None, phone_number: int = None
) -> User:
    try:
        user = db.session.query(User).filter_by(external_id=user_external_id).scalar()

        if not user:
            raise UserNotFoundError(user_external_id)

        if email:
            user.email = email

        if phone_number:
            user.phone_number = phone_number

        user.updated_at = datetime.now()
        db.session.commit()
    except IntegrityError:
        raise EmailAlreadyRegisteredError()

    return user
