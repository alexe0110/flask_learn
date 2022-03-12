import pytest
from application.app import testing_app


@pytest.fixture()
def app():
    app = testing_app()
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

