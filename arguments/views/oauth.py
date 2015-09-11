from flask import abort, url_for, session, flash, redirect
from arguments import app
from arguments import idserver


@app.route("/callback")
def oauth_callback():
    resp = idserver.authorized_response()
    if resp is None:
        abort(403)
    
    session["idserver"] = resp
    idserver.request("api/v1/user/auid/")
    return redirect(url_for("questions"))


@app.route('/login')
def login():
    return idserver.authorize(callback=url_for('oauth_callback', _external=True))
