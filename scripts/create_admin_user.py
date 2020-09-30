from typing import Optional
from getpass import getpass
import transaction
from typer import echo, run, Exit
import sqlalchemy.orm
from ekklesia_common.database import Session
from ekklesia_portal.datamodel import User, UserPassword
from ekklesia_portal.lib.password import password_context


def find_user(session: Session, name: str) -> Optional[User]:
    user = session.query(User).filter_by(name=name).scalar()
    return user


def create_user(session: Session, name: str) -> User:
    user = User(name=name)
    user.password = UserPassword()
    session.add(user)
    return user


def main(name: str, reset_password: bool = False, config: Optional[str] = None):
    from ekklesia_portal.app import make_wsgi_app

    make_wsgi_app(config)

    session = Session()

    user = find_user(session, name)

    if user is None:
        user = create_user(session, name)
        echo(f"User {name} created")
    elif reset_password:
        echo(f"User {name} already exists with id {user.id}, resetting password")
    else:
        echo(f"User {name} already exists with id {user.id}, not resetting password!")
        raise Exit()

    password = getpass()
    user.password.hashed_password = password_context.hash(password, scheme="pbkdf2_sha256")
    input("Press Enter to commit changes to the database, or CTRL-C to abort...")

    transaction.commit()


if __name__ == "__main__":
    run(main)
