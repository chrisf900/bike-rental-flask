from mobility.bike.core import services as bike_services
from users import providers, utils
from users.lib.exceptions import UserNotFoundError


def get_user_by_external_id(user_external_id: int):
    """
    Get a user by external id
    :param user_external_id: int
    :return: User Model
    """
    user = providers.get_user_by_external_id(user_external_id=user_external_id)
    if not user:
        raise UserNotFoundError()
    return user


def get_user_by_email(user_email: str):
    """
    Get a user by email
    :param user_email: str
    :return: User Model
    """
    user = providers.get_user_by_email(user_email=user_email)
    return user


def create_profile(
    first_name: str,
    last_name: str,
    gender: str,
    birthday: str,
    country_code: str,
    email: str,
    phone_number: int,
    password: str,
):
    """
    Create a new profile
    :param first_name: str
    :param last_name: str
    :param gender: str
    :param birthday: str
    :param country_code: str
    :param email: str
    :param phone_number: int
    :param password: str
    :return: User Model
    """
    gender_id = providers.get_gender_by_name(name=gender).id
    country_code = bike_services.get_country_by_code(country_code=country_code).code
    user = providers.create_profile(
        first_name=first_name,
        last_name=last_name,
        gender_id=gender_id,
        birthday=birthday,
        country_code=country_code,
        email=email,
        phone_number=phone_number,
        password=utils.get_password_hash(password=password),
    )
    return user


def update_user_contact_info(
    user_external_id: int,
    email: str = None,
    phone_number: int = None,
):
    """
    Update the user's contact info. Update email or phone number or both
    :param user_external_id: int
    :param email: str = None
    :param phone_number: str = None
    :return: User Model
    """
    user = providers.update_user_contact_info(
        user_external_id=user_external_id, email=email, phone_number=phone_number
    )
    return user
