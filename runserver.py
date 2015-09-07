import os.path
from arguments import make_app

flask_app = make_app()
flask_app.run(host="0.0.0.0", port=5000, debug=True, extra_files=[os.path.join(os.path.dirname(__file__), ".babelcompiled")])
