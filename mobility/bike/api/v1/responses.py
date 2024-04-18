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


class APIUserDoesNotExistError(BaseErrorResponse):
    status_code = HTTPStatus.NOT_FOUND
    error = "API_USER_NOT_FOUND_ERROR"


class APIBikeDoesNotExistError(BaseErrorResponse):
    status_code = HTTPStatus.NOT_FOUND
    error = "API_BIKE_NOT_FOUND_ERROR"


class APIInvalidBikeStatusTransition(BaseErrorResponse):
    status_code = HTTPStatus.CONFLICT
    error = "API_INVALID_BIKE_STATUS_TRANSITION"


class APIUserWithActiveTrip(BaseErrorResponse):
    status_code = HTTPStatus.CONFLICT
    error = "API_USER_WITH_ACTIVE_TRIP"


class APIUserWithNoActiveTrip(BaseErrorResponse):
    status_code = HTTPStatus.CONFLICT
    error = "API_USER_WITH_NO_ACTIVE_TRIP"
