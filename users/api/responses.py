import json
from http import HTTPStatus

from werkzeug import Response


class BaseErrorResponse(Response):
    status_code = HTTPStatus.INTERNAL_SERVER_ERROR
    error = "API_INTERNAL_ERROR"

    def __init__(self, detail=None):
        data = {"message": self.error}
        if detail:
            data["detail"] = detail
        super().__init__(
            response=json.dumps(data),
            status=self.status_code,
            mimetype="application/json",
        )


class APIValidationError(BaseErrorResponse):
    status_code = HTTPStatus.BAD_REQUEST
    error = "API_VALIDATION_ERROR"


class APICountryDoesNotExistsError(BaseErrorResponse):
    status_code = HTTPStatus.NOT_FOUND
    error = "API_COUNTRY_DOES_NOT_EXISTS_ERROR"


class APIIncorrectUserOrPasswordError(BaseErrorResponse):
    status_code = HTTPStatus.UNAUTHORIZED
    error = "Incorrect Username or Password"


class APITokenRevokedError(BaseErrorResponse):
    status_code = HTTPStatus.UNAUTHORIZED
    error = "The token has been revoked."
