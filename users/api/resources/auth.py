from http import HTTPStatus

from flask import Blueprint, jsonify, make_response, request
from flask_jwt_extended import create_access_token, get_jwt, jwt_required
from flask_restx import Api, Resource

from database import RedisClient
from users import utils
from users.api.responses import APIIncorrectUserOrPasswordError, APITokenRevokedError
from users.lib.constants import ACCESS_EXPIRES
from users.lib.exceptions import UserNotFoundError
from users.utils import check_if_token_is_revoked

auth_bp = Blueprint("auth", __name__, url_prefix="/api/v1")
auth = Api(auth_bp)


@auth.route("/login")
class UserLoginResource(Resource):
    def post(self):
        username = request.form.get("username")
        password = request.form.get("password")

        try:
            user = utils.authenticate_user(username, password)
        except UserNotFoundError:
            return APIIncorrectUserOrPasswordError()

        access_token = create_access_token(identity=user.external_id)
        token_response = jsonify(dict(user_id=user.external_id, token=access_token))

        if check_if_token_is_revoked(access_token):
            return APITokenRevokedError()

        return make_response(token_response, HTTPStatus.OK)


@auth.route("/logout")
class UserLogoutResource(Resource):
    @jwt_required()
    def post(self):
        redis_client = RedisClient()

        jti = get_jwt()["jti"]
        redis_client.conn.set(name=jti, value="", ex=ACCESS_EXPIRES)
        token_response = jsonify(dict(message="Successfully logged out"))
        return make_response(token_response, HTTPStatus.OK)
