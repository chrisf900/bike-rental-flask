from datetime import datetime, time
from decimal import Decimal
from uuid import UUID

import overpy
from flask_sqlalchemy.query import Query

from database import db
from mobility.bike.core.models import Bike, PaymentMethod, Trip, User
from mobility.bike.lib.exceptions import BikeNotFoundError, UserNotFoundError


def get_user_by_external_id(user_external_id: int) -> User:
    user = db.session.query(User).filter_by(external_id=user_external_id).scalar()
    if not user:
        raise UserNotFoundError()
    return user


def get_bike_by_bike_code(bike_code: int) -> Bike:
    bike = db.session.query(Bike).filter_by(code=bike_code).scalar()
    if not bike:
        raise BikeNotFoundError()
    return bike


def get_bike_by_uuid(bike_uuid: str | UUID) -> Bike:
    bike = db.session.query(Bike).filter_by(uuid=bike_uuid).scalar()
    if not bike:
        raise BikeNotFoundError()
    return bike


def get_bikes_by_status(status: str) -> Query:
    return db.session.query(Bike).filter_by(status=status, is_active=True)


def get_trips_by_user_uuid(user_uuid: str | UUID) -> Trip:
    return (
        db.session.query(Trip)
        .filter_by(user_uuid=user_uuid)
        .order_by(Trip.created_at.desc())
    )


def get_available_bikes_by_location_and_radius(
    latitude: Decimal | str, longitude: Decimal | str, radius: str
):
    api = overpy.Overpass()
    query = (
        """(node[amenity=bicycle_rental](around:{radius},{lat},{lon}););out;""".format(
            radius=radius, lat=latitude, lon=longitude
        )
    )
    result = api.query(query)
    return result


def get_paginated_query(
    query: Query, page: int, per_page: int, max_per_page: int
) -> Query:
    return db.paginate(
        select=query,
        page=page,
        per_page=per_page,
        max_per_page=max_per_page,
        error_out=True,
    ).items


def get_payment_method_by_name(payment_method_name: str) -> PaymentMethod:
    return db.session.query(PaymentMethod).filter_by(name=payment_method_name).scalar()


def get_current_user_trip(user_uuid: str | UUID) -> Trip:
    return db.session.query(Trip).filter_by(user_uuid=user_uuid, end_time=None).scalar()


def create_trip(
    user_uuid: str | UUID,
    bike_uuid: str | UUID,
    start_lat: str | Decimal,
    start_lon: str | Decimal,
    payment_method_id: str,
) -> Trip:
    trip = Trip(
        user_uuid=user_uuid,
        bike_uuid=bike_uuid,
        start_time=datetime.now(),
        start_lat=start_lat,
        start_lon=start_lon,
        payment_method_id=payment_method_id,
        created_at=datetime.now(),
    )

    db.session.add(trip)
    db.session.commit()

    return trip


def end_trip(
    instance: Trip,
    end_lat: str | Decimal,
    end_lon: str | Decimal,
    time_used: time,
    fare: int,
    calorie: int,
) -> Trip:
    instance.end_time = datetime.now()
    instance.end_lat = end_lat
    instance.end_lon = end_lon
    instance.time_used = time_used
    instance.fare = fare
    instance.calorie = calorie
    instance.updated_at = datetime.now()
    db.session.commit()

    return instance
