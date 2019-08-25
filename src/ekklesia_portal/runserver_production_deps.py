"""
Simplified version of runserver to check if the app runs with production deps only.
"""
import morepath


def run():
    from ekklesia_portal.app import make_wsgi_app
    wsgi_app = make_wsgi_app()
    morepath.run(wsgi_app)


if __name__ == "__main__":
    run()
