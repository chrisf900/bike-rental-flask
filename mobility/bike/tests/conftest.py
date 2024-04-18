import pytest

from app import app


@pytest.fixture()
def test_app():
    with app.app_context():
        app.config.update({"TESTING": True})

    yield app


@pytest.fixture()
def client(test_app):
    with test_app.test_client() as client:
        yield client
