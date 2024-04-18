from datetime import datetime, timezone
from decimal import Decimal
from typing import Any, Dict

from flask_sqlalchemy.query import Query

from mobility.bike.core import providers
from mobility.bike.core.business_logic import BikeStateMachine, get_state_class
from mobility.bike.lib.constants import BASE_FARE, BikeConstants
from mobility.bike.lib.exceptions import (
    BikeNotFoundError,
    InvalidBikeStatusTransition,
    UserWithActiveTrip,
    UserWithNoActiveTrip,
)


def get_paginated_user_trips_by_user(
    user_external_id: int, page: int = 1, per_page: int = 5, max_per_page: int = 5
) -> Query:
    """
    Get paginated user trips
    :param user_external_id: int
    :param page: int = 1
    :param per_page: int = 10
    :param max_per_page: int = 5
    :return: Query
    """
    user = providers.get_user_by_external_id(user_external_id=user_external_id)
    query = providers.get_trips_by_user_uuid(user_uuid=user.uuid)
    trips = providers.get_paginated_query(
        query=query, page=page, per_page=per_page, max_per_page=max_per_page
    )

    return trips


def get_available_bikes_by_location(
    latitude: Decimal | str, longitude: Decimal | str
) -> Dict[str, Any]:
    """
    Get available bikes by latitude and longitude
    :param latitude: Decimal | str
    :param longitude: Decimal | str
    :return: Dict[str, Any]
    """
    query = providers.get_bikes_by_status(status=BikeConstants.AVAILABLE)

    markers = []
    for node in query:
        idd = f"BIKE-{str(node.code)}"
        markers.append([idd, str(node.last_lat), str(node.last_lon)])

    return dict(markers=markers, lat=latitude, lon=longitude)


def update_bike_status(
    bike_instance, status: str, coords: Dict[str, str] = None
) -> None:
    """
    Update the user's bike based on the status entered.
    There are 2 states handled by a state machine:
    'available' | 'unavailable'
    :param bike_instance: Bike
    :param status: str
    :param coords: List[str] = None
    :return: None
    """
    if status.upper() == bike_instance.status:
        raise InvalidBikeStatusTransition()

    old_state_class = get_state_class(state=bike_instance.status)
    new_state_class = get_state_class(state=status.upper())

    bsm = BikeStateMachine(state=old_state_class, bike=bike_instance, coords=coords)
    bsm.change(new_state_class)


def start_trip(
    user_external_id: int,
    bike_code: str | int,
    payment_method_name: str,
) -> Query:
    """
    Start the user's trip. This unlocks the bicycle
    :param user_external_id: int
    :param bike_code: str
    :param payment_method_name: str
    :return: Query
    """
    bike_code = bike_code.split("-")[1]
    if not bike_code.isnumeric():
        raise BikeNotFoundError()

    bike = providers.get_bike_by_bike_code(bike_code=int(bike_code))
    payment_method = providers.get_payment_method_by_name(
        payment_method_name=payment_method_name
    )
    user = providers.get_user_by_external_id(user_external_id=user_external_id)
    current_trip = providers.get_current_user_trip(user_uuid=user.uuid)

    if current_trip:
        raise UserWithActiveTrip()

    trip = providers.create_trip(
        user_uuid=user.uuid,
        bike_uuid=bike.uuid,
        start_lat=bike.last_lat,
        start_lon=bike.last_lon,
        payment_method_id=payment_method.id,
    )

    update_bike_status(bike_instance=bike, status=BikeConstants.UNAVAILABLE)

    return trip


def end_trip(
    user_external_id: int,
    end_lat: Decimal | str,
    end_lon: Decimal | str,
) -> Query:
    """
    Ends the user's trip. This locks the bicycle
    :param user_external_id: int
    :param end_lon: Decimal | str
    :param end_lat: Decimal | str
    :return: Query
    """
    user = providers.get_user_by_external_id(user_external_id=user_external_id)
    current_trip = providers.get_current_user_trip(user_uuid=user.uuid)

    if not current_trip:
        raise UserWithNoActiveTrip()

    bike = providers.get_bike_by_uuid(bike_uuid=current_trip.bike_uuid)

    end_time = datetime.now(timezone.utc)
    time_used = end_time - current_trip.start_time
    time_used_in_seconds = time_used.total_seconds() / 60

    calorie = int(time_used_in_seconds * 4.16)
    fare = int(time_used_in_seconds * BASE_FARE)

    trip = providers.end_trip(
        instance=current_trip,
        end_lat=end_lat,
        end_lon=end_lon,
        time_used=time_used,
        fare=fare,
        calorie=calorie,
    )

    update_bike_status(
        bike_instance=bike,
        status=BikeConstants.AVAILABLE,
        coords={"lat": end_lat, "lon": end_lon},
    )

    return trip
