#from flask import flash, redirect, url_for
#from flask_login import login_required, logout_user
#from flask.ext.babelex import _

from ekklesia_portal import app


#@app.route("/logout")
#@login_required
def logout():
    logout_user()
    flash(_("logged_out"))
    return redirect(url_for("propositions"))
