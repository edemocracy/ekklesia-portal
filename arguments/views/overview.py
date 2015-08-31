from flask import render_template
from arguments import app


@app.route("/")
def overview():
    return render_template("overview.j2.jade")
