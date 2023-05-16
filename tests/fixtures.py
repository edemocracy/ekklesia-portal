import logging
import os
from pathlib import Path
from ekklesia_common.database import Session
from ekklesia_common.request import EkklesiaRequest
from morepath.request import BaseRequest
from munch import Munch
from pytest import fixture
from webtest import TestApp as Client

from ekklesia_portal.app import make_wsgi_app, App
from ekklesia_portal.datamodel import DepartmentMember, Proposition, User
from ekklesia_portal.enums import ArgumentType
from ekklesia_portal.identity_policy import UserIdentity

ROOT_DIR = Path(__file__).absolute().parent.parent
logg = logging.getLogger(__name__)


@fixture
def fixture_by_name(request):
    return request.getfixturevalue(request.param)


def get_db_uri():
    return os.getenv('EKKLESIA_PORTAL_TEST_DB_URL',
        'postgresql+psycopg2:///test_ekklesia_portal?host=/tmp')


def get_test_settings(db_uri):
    return {
        'database': {
            'uri': db_uri
        },
        'app': {
            'default_language': 'en',
            'languages': ['en', 'de']
        },
        'test_section': {
            'test_setting': 'test'
        },
        'common': {
            'instance_name': 'test',
            'fail_on_form_validation_error': False
        },
        'browser_session': {
            'secret_key': 'test',
            'cookie_secure': False
        },
        'ekklesia_auth': {
            'client_id': 'client_id_test',
            'client_secret': 'test_secret',
            'authorization_url': 'http://id.invalid/openid-connect/auth',
            'token_url': 'http://id.invalid/openid-connect/token',
            'userinfo_url': 'http://id.invalid/openid-connect/userinfo'
        },
        'importer': {
            'test': {
                'schema': 'test_source',
                'base_url': 'test'
            }
        },

        'share': {
            'use_url_shortener': False
        },
        'voting_modules': {
            "test": {
                'api_urls': [
                  "http://vvvote1", "http://vvvote2"
                ],
                'defaults': {
                    'must_be_eligible': True,
                    'must_be_verified': False,
                    'auth_server_id': 'test_auth_server',
                    'required_role': 'test_role',
                }
            }
        }
    }

@fixture(scope="session")
def settings():
    return get_test_settings(get_db_uri())


@fixture(scope="session")
def app(settings):
    App.init_settings(settings)
    app = make_wsgi_app(testing=True)
    return app


@fixture
def client(app):
    return Client(app)


@fixture
def req(app):
    environ = BaseRequest.blank('test').environ
    req = EkklesiaRequest(environ, app)
    req.i18n = Munch(dict(gettext=(lambda s, *a, **k: s)))
    req.browser_session = {}
    return req


@fixture
def db_session(app):
    session = Session()
    yield session
    session.rollback()


@fixture
def db_query(db_session):
    return db_session.query


@fixture
def proposition_with_arguments(user, user_two, proposition, argument_factory, argument_relation_factory):
    arg1 = argument_factory(author=user, title='Ein Pro-Argument', abstract='dafür abstract', details='dafür')
    arg2 = argument_factory(author=user_two, title='Ein zweites Pro-Argument', abstract='dafür!!!')
    arg3 = argument_factory(author=user, title='Ein Contra-Argument', abstract='dagegen!!!', details='aus Gründen')
    arg1_rel = argument_relation_factory(proposition=proposition, argument=arg1, argument_type=ArgumentType.PRO)
    arg2_rel = argument_relation_factory(proposition=proposition, argument=arg2, argument_type=ArgumentType.PRO)
    arg3_rel = argument_relation_factory(proposition=proposition, argument=arg3, argument_type=ArgumentType.CONTRA)
    return proposition


@fixture
def user_with_departments(user_factory, department_factory):
    user = user_factory()
    departments = [department_factory(), department_factory()]
    user.departments = departments

    for department in departments:
        user.areas.extend(department.areas)

    return user


def refresh_user_object(user):
    return user


@fixture
def logged_in_user(user, monkeypatch):
    user_identity = UserIdentity(user, refresh_user_object)
    monkeypatch.setattr('ekklesia_common.request.EkklesiaRequest.identity', user_identity)
    return user


@fixture
def logged_in_user_with_departments(user_with_departments, monkeypatch):
    user = user_with_departments
    user_identity = UserIdentity(user, refresh_user_object)
    monkeypatch.setattr('ekklesia_common.request.EkklesiaRequest.identity', user_identity)
    return user


@fixture
def global_admin(group_factory, user_factory):
    user = user_factory()
    group = group_factory()
    group.members.append(user)
    return user


@fixture
def department_admin(db_session, user_factory, department_factory):
    user = user_factory()
    d1 = department_factory(description='admin')
    d2 = department_factory(description='not admin')
    dm = DepartmentMember(member=user, department=d1, is_admin=True)
    db_session.add(dm)
    user.departments.append(d2)
    return user


@fixture
def logged_in_department_admin(department_admin, monkeypatch):
    user_identity = UserIdentity(department_admin, refresh_user_object, has_global_admin_permissions=False)
    monkeypatch.setattr('ekklesia_common.request.EkklesiaRequest.identity', user_identity)
    return department_admin


@fixture
def logged_in_global_admin(global_admin, monkeypatch):
    user_identity = UserIdentity(global_admin, refresh_user_object, has_global_admin_permissions=True)
    monkeypatch.setattr('ekklesia_common.request.EkklesiaRequest.identity', user_identity)
    return global_admin


@fixture(autouse=True)
def no_db_commit(monkeypatch):

    def dummy_commit(*a, **kw):
        logg.debug('would commit now')

    monkeypatch.setattr('transaction.manager.commit', dummy_commit)
