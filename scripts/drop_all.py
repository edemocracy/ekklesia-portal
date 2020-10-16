import argparse
import logging
from datetime import datetime
import os

from alembic.config import Config
from alembic import command
import mimesis
import sqlalchemy.orm
import transaction
from ekklesia_common.ekklesia_auth import OAuthToken

from ekklesia_portal.app import make_wsgi_app
from ekklesia_portal.enums import ArgumentType, Majority, PropositionStatus, SupporterStatus, VotingStatus, VotingSystem, VotingType
from ekklesia_portal.lib.password import password_context

logging.basicConfig(level=logging.INFO)

parser = argparse.ArgumentParser("Ekklesia Portal create_test_db.py")
parser.add_argument("-c", "--config-file", help=f"path to config file in YAML / JSON format")

if __name__ == "__main__":

    logg = logging.getLogger(__name__)

    args = parser.parse_args()

    app = make_wsgi_app(args.config_file)

    # Needed for Alembic env.py
    if args.config_file:
        os.environ['EKKLESIA_PORTAL_CONFIG'] = args.config_file
    if 'EKKLESIA_PORTAL_CONFIG' not in os.environ:
        os.environ['EKKLESIA_PORTAL_CONFIG'] = "config.yml"

    from ekklesia_common.database import db_metadata, Session
    # local import because we have to set up the database stuff before that
    from ekklesia_portal.datamodel import (
        Argument, ArgumentRelation, ArgumentVote, Ballot, CustomizableText, Department, DepartmentMember, Document,
        Group, Policy, Proposition, PropositionType, SubjectArea, Supporter, Tag, User, UserPassword, UserProfile,
        VotingPhase, VotingPhaseType
    )

    print(f"using config file {args.config_file}")
    print(f"using db url {app.settings.database.uri}")

    engine = sqlalchemy.create_engine(app.settings.database.uri)
    connection = engine.connect()
    connection.execute("select")

    sqlalchemy.orm.configure_mappers()

    print(80 * "=")
    input("press Enter to drop all tables...")

    db_metadata.drop_all()
    connection.execute("DROP TABLE IF EXISTS alembic_version")

    transaction.commit()

    logg.info("committed")
