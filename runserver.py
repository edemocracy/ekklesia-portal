import datetime
import os.path
from arguments import make_app
import tempfile

tmpdir = tempfile.gettempdir()

flask_app = make_app()

with open(os.path.join(tmpdir, "arguments.started"), "w") as wf:
    wf.write(datetime.datetime.now().isoformat())
    wf.write("\n")


flask_app.run(host="0.0.0.0", port=5000, debug=True, extra_files=[os.path.join(os.path.dirname(__file__), ".babelcompiled")])
