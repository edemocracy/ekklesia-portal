from os import path
from morepath.request import BaseRequest
from pytest import fixture
from webtest import TestApp as Client
from arguments.app import make_wsgi_app, CustomRequest
from arguments.database import Session
from arguments.database.datamodel import Proposition


BASEDIR = path.dirname(__file__)


@fixture(scope="session")
def config_filepath():
    return path.join(BASEDIR, "testconfig.yml")


@fixture(scope="session")
def app(config_filepath):
    app = make_wsgi_app(config_filepath)
    return app


@fixture(scope="session")
def client(app):
    return Client(app)


@fixture
def request(app):
    environ = BaseRequest.blank('test').environ
    return CustomRequest(environ, app)


@fixture
def session(app):
    return Session()


@fixture
def proposition(session):
    return session.query(Proposition).get(1)
