from flask_restx import Api

from mobility.bike.api.v1.resources.bike import api as bike_resource
from mobility.bike.api.v1.resources.user_trip import api as user_trip_resource

api = Api(title="Bike Rental API", version="1.0", doc="/docs")

api.add_namespace(bike_resource, path="/bike-rental/api/v1")
api.add_namespace(user_trip_resource, path="/bike-rental/api/v1")
