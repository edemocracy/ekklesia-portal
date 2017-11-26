from arguments.app import App

import morepath
from pytest import fixture
from webtest import TestApp as Client

@fixture(scope="session")
def app():
    morepath.autoscan()
    App.commit()
    return App()


@fixture(scope="session")
def client(app):
    return Client(app)


def test_index(client):
    res = client.get("/")
    assert res.body

