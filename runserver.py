from arguments import make_app

flask_app = make_app()
flask_app.run(host="0.0.0.0", port=5000, debug=True)
