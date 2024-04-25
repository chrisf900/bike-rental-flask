from http import HTTPStatus

from flask import make_response, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restx import Namespace, Resource
from marshmallow import ValidationError

from mobility.bike.api.v1.responses import APIValidationError
from mobility.bike.api.v1.schemas import SearchCoordinatesSchema
from mobility.bike.core import services

api = Namespace("BikeResource", description="Bike Map")


@api.route("/bikes")
class BikeResource(Resource):
    validator_class = SearchCoordinatesSchema()

    @jwt_required()
    def post(self):
        try:
            data = self.validator_class.load(data=request.form)

            bikes = services.get_available_bikes_by_location(
                latitude=data["latitude"],
                longitude=data["longitude"],
            )
        except ValidationError as err:
            return APIValidationError(err.messages)

        return make_response(bikes, HTTPStatus.OK)
