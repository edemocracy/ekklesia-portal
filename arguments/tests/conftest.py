from os import path
from pytest import fixture
from webtest import TestApp as Client
from munch import Munch
from morepath.request import BaseRequest
from arguments.app import make_wsgi_app, CustomRequest


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
