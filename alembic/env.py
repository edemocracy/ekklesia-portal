import logging
from logging.config import fileConfig

from sqlalchemy import create_engine
from sqlalchemy import pool

from alembic import context

import ekklesia_common.database
from ekklesia_portal.app import get_database_uri_for_alembic

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

target_metadata = ekklesia_common.database.Base.metadata

logg = logging.getLogger(__name__)


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = get_database_uri_for_alembic()

    context.configure(
        url=url,
        target_metadata=target_metadata,
        compare_type=True,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    external_connection = config.attributes.get('connection', None)
    if external_connection is None:
        url = get_database_uri_for_alembic()
        logg.info("Creating an engine for database URL %s", url)
        engine = create_engine(url, poolclass=pool.NullPool)
        connection = engine.connect()
    else:
        logg.info("Using supplied external connection %s", external_connection)
        connection = external_connection

    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        compare_server_default=True)

    with context.begin_transaction():
        context.run_migrations()

    if external_connection is None:
        connection.close()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
