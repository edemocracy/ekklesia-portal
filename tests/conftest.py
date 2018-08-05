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

logging.basicConfig(level=logging.DEBUG)
logging.getLogger('morepath').setLevel(logging.INFO)

logg = logging.getLogger('test')

BASEDIR = path.dirname(__file__)

from .factories import *

@fixture(scope="session")
def config_filepath():
    return path.join(BASEDIR, "testconfig.yml")


@fixture(scope="session")
def app(config_filepath):
    app = make_wsgi_app(config_filepath, testing=True)
    return app


@fixture(scope="session")
def client(app):
    return Client(app)


@fixture
def req(app):
    environ = BaseRequest.blank('test').environ
    return EkklesiaPortalRequest(environ, app)


@fixture
def db_session(app):
    return Session()


@fixture
def proposition_with_arguments(user, user_two, proposition, argument_factory, argument_relation_factory):
    arg1 = argument_factory(author=user, title='Ein Pro-Argument', abstract='dafür abstract', details='dafür')
    arg2 = argument_factory(author=user_two, title='Ein zweites Pro-Argument', abstract='dafür!!!')
    arg3 = argument_factory(author=user, title='Ein Contra-Argument', abstract='dagegen!!!', details='aus Gründen')
    arg1_rel = argument_relation_factory(proposition=proposition, argument=arg1, argument_type='pro')
    arg2_rel = argument_relation_factory(proposition=proposition, argument=arg2, argument_type='pro')
    arg3_rel = argument_relation_factory(proposition=proposition, argument=arg3, argument_type='con')
    return proposition


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
