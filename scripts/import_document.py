import argparse

import transaction
import sqlalchemy.orm
from ekklesia_common.database import Session
from eliot import start_action

from ekklesia_portal.datamodel import Department, Document, SubjectArea


def load_document_content(filepath) -> str:
    with open(filepath) as f:
        with start_action(log_level="INFO", action_type="load_file"):
            content = f.read()

    return content


def find_document(name: str, department: str) -> Document:
    with start_action(action_type="find_document", name=name, department=department) as action:
        document = session.query(Document).filter_by(name=name).join(SubjectArea).join(Department).filter_by(name=department).one()

        if document is None:
            raise ValueError(f"Document {args.name} in department {args.department} not found!")

        action.add_success_fields(document_id=document.id)

    return document


parser = argparse.ArgumentParser("Ekklesia Portal import_election_program.py")
parser.add_argument("-c", "--config-file", help=f"Path to config file in YAML / JSON format")
parser.add_argument("-f", "--filepath", help=f"Choose the filepath to import from.", required=True)
parser.add_argument("--name", help=f"Document name", required=True)
parser.add_argument("--department", help=f"Choose the department to import to.", required=True)

if __name__ == "__main__":
    args = parser.parse_args()

    from ekklesia_portal.app import make_wsgi_app

    app = make_wsgi_app(args.config_file)

    session = Session()
    session.autoflush = True

    sqlalchemy.orm.configure_mappers()

    content = load_document_content(args.filepath)
    document = find_document(args.name, args.department)

    document.text = content

    #input("Press Enter to commit changes to the database, or CTRL-C to abort...")

    transaction.commit()
