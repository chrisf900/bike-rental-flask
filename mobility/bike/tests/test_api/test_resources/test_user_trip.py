from http import HTTPStatus

import pytest

from mobility.bike.lib.exceptions import (
    BikeNotFoundError,
    InvalidBikeStatusTransition,
    UserNotFoundError,
    UserWithActiveTrip,
)

URL_PATH = "/bike-rental/api/v1/users/{}/trips".format(416000)


def test_get_user_trip(mocker, client):
    mock_get_paginated_user_trips = mocker.patch(
        "mobility.bike.api.v1.resources.user_trip.services.get_paginated_user_trips_by_user"
    )
    response = client.get(URL_PATH.format(416000))
    assert response.status_code == HTTPStatus.OK

    mock_get_paginated_user_trips.side_effect = UserNotFoundError
    response = client.get(URL_PATH.format(416000))
    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.parametrize(
    "exception, status_code_expected",
    [
        (UserNotFoundError, HTTPStatus.NOT_FOUND),
        (BikeNotFoundError, HTTPStatus.NOT_FOUND),
        (UserWithActiveTrip, HTTPStatus.CONFLICT),
        (InvalidBikeStatusTransition, HTTPStatus.CONFLICT),
    ],
)
def test_post_user_trip(mocker, client, exception, status_code_expected):
    mock_start_trip = mocker.patch(
        "mobility.bike.api.v1.resources.user_trip.services.start_trip", return_value=[]
    )
    data = {"bike_code": "BIKE-1234", "payment_method_name": "Visa Credit Card"}

    response = client.post(URL_PATH.format(416000), data=data)
    assert response.status_code == HTTPStatus.BAD_REQUEST

    data["payment_method_name"] = "Credit Card"

    response = client.post(URL_PATH.format(416000), data=data)
    assert response.status_code == HTTPStatus.OK

    mock_start_trip.side_effect = exception
    response = client.post(URL_PATH.format(416000), data=data)
    assert response.status_code == status_code_expected


def test_patch_user_trip(mocker, client):
    mocker.patch(
        "mobility.bike.api.v1.resources.user_trip.services.end_trip", return_value=[]
    )
    data = {"end_latitude": "-33.44021", "end_longitude": "-70.44021"}
    response = client.patch(URL_PATH.format(416000), data=data)
    assert response.status_code == HTTPStatus.OK

    data["end_latitude"] = "3344021"
    response = client.post(URL_PATH.format(416000), data=data)
    assert response.status_code == HTTPStatus.BAD_REQUEST
