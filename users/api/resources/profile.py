from http import HTTPStatus

from flask import Blueprint, make_response, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restx import Api, Resource
from marshmallow import ValidationError

from mobility.bike.lib.exceptions import CountryNotFoundError
from users import services
from users.api.responses import APICountryDoesNotExistsError, APIValidationError
from users.api.schemas import CreateUserSchema, UpdateUserContactInfoSchema, UserSchema

profile_bp = Blueprint("profile", __name__, url_prefix="/api/v1")
profile = Api(
    profile_bp,
    title="User Profile API",
    default="ProfileResource",
    default_label="User Profile",
    doc="/docs",
)


@profile.route("/profile")
class ProfileResource(Resource):
    serializer_class = UserSchema()

    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity()
        user = services.get_user_by_external_id(user_external_id=current_user_id)

        user_response = self.serializer_class.dump(user)
        return make_response(user_response, HTTPStatus.OK)

    @profile.doc(
        params={
            "first_name": "",
            "last_name": "",
            "email": "",
            "phone_number": "",
            "country_code": "",
            "birthday": "YYYY/MM/DD",
            "gender": "Male/Female",
            "password": "",
        }
    )
    def post(self):
        validator_class = CreateUserSchema()

        try:
            data = validator_class.load(data=request.form)
            user = services.create_profile(
                first_name=data["first_name"],
                last_name=data["last_name"],
                gender=data["gender"],
                birthday=data["birthday"],
                country_code=data["country_code"],
                email=data["email"],
                phone_number=data["phone_number"],
                password=data["password"],
            )
        except ValidationError as err:
            return APIValidationError(err.messages)
        except CountryNotFoundError:
            return APICountryDoesNotExistsError()

        user_response = self.serializer_class.dump(user)
        return make_response(user_response, HTTPStatus.CREATED)

    @profile.doc(params={"email": "", "phone_number": ""})
    @jwt_required()
    def patch(self):
        validator_class = UpdateUserContactInfoSchema()
        try:
            current_user_uuid = get_jwt_identity()
            data = validator_class.load(data=request.form)

            user = services.update_user_contact_info(
                user_external_id=current_user_uuid,
                email=data.get("email"),
                phone_number=data.get("phone_number"),
            )
        except ValidationError as err:
            return APIValidationError(err.messages)

        user_response = self.serializer_class.dump(user)
        return make_response(user_response, HTTPStatus.OK)
