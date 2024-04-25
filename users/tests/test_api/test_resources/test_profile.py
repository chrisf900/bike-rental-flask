from http import HTTPStatus

import pytest

from mobility.bike.lib.exceptions import CountryNotFoundError

URL_PATH = "/api/v1/profile"


def test_get_profile(mocker, client):
    mocker.patch("flask_jwt_extended.view_decorators.verify_jwt_in_request")
    mocker.patch("users.api.resources.profile.get_jwt_identity")
    mocker.patch(
        "users.api.resources.profile.services.get_user_by_external_id", return_value=[]
    )
    response = client.get(URL_PATH)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    "exception, status_code_expected",
    [
        (CountryNotFoundError, HTTPStatus.NOT_FOUND),
    ],
)
def test_post_profile(mocker, client, exception, status_code_expected):
    mocker.patch("flask_jwt_extended.view_decorators.verify_jwt_in_request")
    mock_start_trip = mocker.patch(
        "users.api.resources.profile.services.create_profile", return_value=[]
    )
    data = {
        "first_name": "John",
        "last_name": "Doe",
        "gender": "Male",
        "birthday": "2022-02-22",
        "country_code": "CL",
        "email": "johndoe.com",
        "phone_number": 987654321,
        "password": "johndoe",
    }

    response = client.post(URL_PATH, data=data)
    assert response.status_code == HTTPStatus.BAD_REQUEST

    data["email"] = "john@doe.com"

    response = client.post(URL_PATH, data=data)
    assert response.status_code == HTTPStatus.CREATED

    mock_start_trip.side_effect = exception
    response = client.post(URL_PATH, data=data)
    assert response.status_code == status_code_expected


def test_patch_profile(mocker, client):
    mocker.patch("flask_jwt_extended.view_decorators.verify_jwt_in_request")
    mocker.patch("users.api.resources.profile.get_jwt_identity")
    mocker.patch(
        "users.api.resources.profile.services.update_user_contact_info", return_value=[]
    )
    data = {"email": "john@doe.com", "phone_number": "9999999"}
    response = client.patch(URL_PATH, data=data)
    assert response.status_code == HTTPStatus.OK

    data["email"] = "johndoe1"
    response = client.post(URL_PATH, data=data)
    assert response.status_code == HTTPStatus.BAD_REQUEST
