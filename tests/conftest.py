import logging
import os
from os import path
import sys
from morepath.request import BaseRequest
from pytest import fixture
from webtest import TestApp as Client
from ekklesia_portal.app import make_wsgi_app
from ekklesia_portal.identity_policy import UserIdentity
from ekklesia_portal.request import EkklesiaPortalRequest
from ekklesia_portal.database import Session
from ekklesia_portal.database.datamodel import Proposition, User

sys.path.append(os.path.join(os.path.dirname(__file__), 'helpers'))

import logging
logging.basicConfig(level=logging.DEBUG)
logging.getLogger('morepath').setLevel(logging.INFO)

logg = logging.getLogger('test')

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
    return EkklesiaPortalRequest(environ, app)


@fixture
def db_session(app):
    return Session()


@fixture
def proposition(db_session):
    return db_session.query(Proposition).get(1)


@fixture
def user(db_session):
    return db_session.query(User).get(1)


@fixture
def logged_in_user(user, monkeypatch):
    user_identity = UserIdentity(user)
    monkeypatch.setattr('ekklesia_portal.request.EkklesiaPortalRequest.identity', user_identity)
    return user

@fixture
def no_db_commit(monkeypatch):
    def dummy_commit(*a, **kw):
        logg.info('would commit now')

    monkeypatch.setattr('transaction.manager.commit', dummy_commit)
