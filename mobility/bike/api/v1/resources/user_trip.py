from http import HTTPStatus

from flask import make_response, request
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
    UserNotFoundError,
    UserWithActiveTrip,
    UserWithNoActiveTrip,
)

api = Namespace("UserTripResource", description="User Trip")


@api.route("/users/<int:user_external_id>/trips")
class UserTripResource(Resource):
    list_serializer_class = UserTripSchema()
    serializer_class = TripSchema()

    def get(self, user_external_id):
        page_param = int(request.args.get("page", 1))

        try:
            trips = services.get_paginated_user_trips_by_user(
                user_external_id=user_external_id, page=page_param
            )
        except UserNotFoundError:
            return APIUserDoesNotExistError()

        trip_page = self.list_serializer_class.dump(trips, many=True)
        return make_response(trip_page, HTTPStatus.OK)

    def post(self, user_external_id):
        validator_class = AddTripDataSchema()

        try:
            data = validator_class.load(data=request.form)
            trip = services.start_trip(
                user_external_id=user_external_id,
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

    def patch(self, user_external_id):
        validator_class = AddEndCoordinatesSchema()

        try:
            data = validator_class.load(data=request.form)
            trip = services.end_trip(
                user_external_id=user_external_id,
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
