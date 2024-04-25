from http import HTTPStatus


def test_bike_resource(mocker, client):
    mocker.patch("flask_jwt_extended.view_decorators.verify_jwt_in_request")
    mocker.patch(
        "mobility.bike.api.v1.resources.bike.services.get_available_bikes_by_location"
    )
    data = {"latitude": "-33.44021", "longitude": "-70.44021"}
    response = client.post("/bike-rental/api/v1/bikes", data=data)
    assert response.status_code == HTTPStatus.OK

    data["latitude"] = "3344021"
    response = client.post("/bike-rental/api/v1/bikes", data=data)
    assert response.status_code == HTTPStatus.BAD_REQUEST
