import random
import string

import morepath
from eliot import log_call, start_action
from morepath import Response, redirect

from ekklesia_portal.app import App
from ekklesia_portal.datamodel import User, UserLoginToken

from ..cell.token import TokenCell
from ..contracts.token import TokenForm


@App.path(model=UserLoginToken, path="/token/{token}")
@log_call
def login(request, token):
    return request.q(UserLoginToken).get(token)


@App.html(model=UserLoginToken)
@log_call
def token_login(self, request):
    form = TokenForm(request, request.link(self))
    return TokenCell(request, form, model=self).show()


@App.html_form_post(model=UserLoginToken, form=TokenForm, cell=TokenCell)
@log_call
def submit_token_login(self, request, appstruct):

    if self.user is None:
        with start_action(action_type='create_user', created_by='token', token=self.token) as action:
            name = "user_" + "".join(random.choice(string.ascii_lowercase) for x in range(10))
            user = User(name=name, auth_type='token', login_token=self)
            request.db_session.add(user)
            request.db_session.flush()

            action.add_success_fields(user={'id': user.id, 'name': user.name})

    @request.after
    def remember(response):
        identity = morepath.Identity(self.user.id, user=self.user)
        request.app.remember_identity(response, request, identity)

    return redirect('/')
