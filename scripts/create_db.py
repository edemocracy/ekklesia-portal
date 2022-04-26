import argparse
import logging

from alembic.config import Config
from alembic import command
import sqlalchemy.orm
from sqlalchemy import pool
import transaction

from ekklesia_portal.app import make_wsgi_app
from ekklesia_portal.lib.password import password_context

logging.basicConfig(level=logging.INFO)

parser = argparse.ArgumentParser("Ekklesia Portal create_db.py")
parser.add_argument(
    "-c",
    "--config-file",
    help=f"Optional path to config file in YAML / JSON format. Uses default test configuration when not set."
)
parser.add_argument("--doit", action="store_true", default=False)
parser.add_argument("--lang", default="de", help="The language to create the customizable texts for")

if __name__ == "__main__":

    logg = logging.getLogger(__name__)

    args = parser.parse_args()

    app = make_wsgi_app(args.config_file)

    from ekklesia_common.database import db_metadata, Session
    # local import because we have to set up the database stuff before that
    from ekklesia_portal.datamodel import CustomizableText, Group, User, UserPassword

    print(f"using config file {args.config_file}")
    print(f"using db url {app.settings.database.uri}")

    engine = sqlalchemy.create_engine(app.settings.database.uri, poolclass=pool.NullPool)
    connection = engine.connect()
    connection.execute("select")

    sqlalchemy.orm.configure_mappers()

    if not args.doit:
        print(80 * "=")
        input("press Enter to drop and create the database...")

    db_metadata.drop_all()
    connection.execute("DROP TABLE IF EXISTS alembic_version")
    db_metadata.create_all()

    s = Session()

    s.add(CustomizableText(lang=args.lang, name='push_draft_external_template', text='TODO: External draft template here'))
    s.add(CustomizableText(lang=args.lang, name='push_draft_portal_template', text='TODO: Portal draft template here'))
    s.add(
        CustomizableText(
            lang=args.lang, name='document_propose_change_explanation', text='TODO: Propose change to document explanation here'
        )
    )
    s.add(CustomizableText(lang=args.lang, name='new_draft_explanation', text='TODO: New draft explanation here'))
    s.add(CustomizableText(lang=args.lang, name='submit_draft_explanation', text='TODO: Submit draft explanation here'))
    s.add(CustomizableText(lang=args.lang, name='ekklesia_login_explanation', text='TODO: Login explanation here'))

    admin_group = Group(name="Admins", is_admin_group=True)
    s.add(admin_group)

    admin = User(name="admin", auth_type="system")
    admin.password = UserPassword(hashed_password=password_context.hash("admin", scheme="plaintext"))
    admin_group.members.append(admin)

    transaction.commit()

    logg.info("committed")

    alembic_cfg = Config("./alembic.ini")
    alembic_cfg.attributes['connection'] = connection

    command.stamp(alembic_cfg, "head")

    # Fixes a strange error message when the connection isn't closed.
    # Didn't happen before.
    connection.close()

    logg.info("finished")
