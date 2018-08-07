if __name__ == "__main__":
    from munch import Munch
    from ekklesia_portal.app import make_wsgi_app

    app = make_wsgi_app("config.yml")
    from ekklesia_portal import database
    from ekklesia_portal.app import App
    from ekklesia_portal.database.datamodel import *

    from tests.factories import *

    s = database.Session()
    q = s.query

    ip = get_ipython() # type: ignore

    ip.magic("autocall 2")
