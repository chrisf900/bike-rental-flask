from http import HTTPStatus

from flask import make_response, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restx import Namespace, Resource
from marshmallow import ValidationError

from mobility.bike.api.v1.responses import (
    APIBikeDoesNotExistError,
    APIInvalidBikeStatusTransition,
    APIUserDoesNotExistError,
    APIUserWithActiveTrip,
    APIUserWithNoActiveTrip,
    APIValidationError,
)
from mobility.bike.api.v1.schemas import (
    AddEndCoordinatesSchema,
    AddTripDataSchema,
    TripSchema,
    UserTripSchema,
)
from mobility.bike.core import services
from mobility.bike.lib.exceptions import (
    BikeNotFoundError,
    InvalidBikeStatusTransition,
    UserWithActiveTrip,
    UserWithNoActiveTrip,
)
from users.lib.exceptions import UserNotFoundError
from users import services as user_services

api = Namespace("UserTripResource", description="User Trip")


@api.route("/users/<int:user_external_id>/trips")
class UserTripResource(Resource):
    list_serializer_class = UserTripSchema()
    serializer_class = TripSchema()

    @jwt_required()
    def get(self, user_external_id):
        page_param = int(request.args.get("page", 1))
        user = self.user_from_request(user_external_id)

        try:
            trips = services.get_paginated_user_trips_by_user(
                user_uuid=user.uuid, page=page_param
            )
        except UserNotFoundError:
            return APIUserDoesNotExistError()

        trip_page = self.list_serializer_class.dump(trips, many=True)
        return make_response(trip_page, HTTPStatus.OK)

    @jwt_required()
    def post(self, user_external_id):
        validator_class = AddTripDataSchema()
        user = self.user_from_request(user_external_id)

        try:
            data = validator_class.load(data=request.form)
            trip = services.start_trip(
                user_uuid=user.uuid,
                bike_code=data["bike_code"],
                payment_method_name=data["payment_method_name"],
            )
        except ValidationError as err:
            return APIValidationError(err.messages)
        except UserNotFoundError:
            return APIUserDoesNotExistError()
        except BikeNotFoundError:
            return APIBikeDoesNotExistError()
        except UserWithActiveTrip:
            return APIUserWithActiveTrip()
        except InvalidBikeStatusTransition:
            return APIInvalidBikeStatusTransition()

        trip_response = self.serializer_class.dump(trip)
        return make_response(trip_response, HTTPStatus.OK)

    @jwt_required()
    def patch(self, user_external_id):
        validator_class = AddEndCoordinatesSchema()
        user = self.user_from_request(user_external_id)

        try:
            data = validator_class.load(data=request.form)
            trip = services.end_trip(
                user_uuid=user.uuid,
                end_lat=data["end_latitude"],
                end_lon=data["end_longitude"],
            )
        except ValidationError as err:
            return APIValidationError(err.messages)
        except UserNotFoundError:
            return APIUserDoesNotExistError()
        except BikeNotFoundError:
            return APIBikeDoesNotExistError()
        except UserWithNoActiveTrip:
            return APIUserWithNoActiveTrip()
        except InvalidBikeStatusTransition:
            return APIInvalidBikeStatusTransition()

        trip_response = self.serializer_class.dump(trip)
        return make_response(trip_response, HTTPStatus.OK)

    def user_from_request(self, user_external_id: int):
        current_user_id = get_jwt_identity()
        user = user_services.get_user_by_external_id(user_external_id)

        if current_user_id != user.external_id:
            return APIUserDoesNotExistError()

        return user
