import pathlib
import sys
import os

import alembic
from sqlalchemy import engine_from_config, create_engine, pool
from psycopg2 import DatabaseError

from logging.config import fileConfig
import logging

# we're appending the app directory to our path here so that we can import config easily
sys.path.append(str(pathlib.Path(__file__).resolve().parents[3]))

from app.core.config import DATABASE_URL, POSTGRES_DB  # noqa

# Alembic Config object, which provides access to values within the .ini file
config = alembic.context.config

# Interpret the config file for logging
fileConfig(config.config_file_name)
logger = logging.getLogger("alembic.env")

target_metadata = None

def run_migrations_online() -> None:
    """
    Run migrations in 'online' mode
    """
    DB_URL = f"{DATABASE_URL}_test" if os.environ.get("TESTING") else str(DATABASE_URL)

    # handle testing config for migrations
    if os.environ.get("TESTING"):
        # connect to primary db
        default_engine = create_engine(str(DATABASE_URL), isolation_level="AUTOCOMMIT")
        # drop testing db if it exists and create a fresh one
        with default_engine.connect() as default_conn:
            default_conn.execute(f"DROP DATABASE IF EXISTS {POSTGRES_DB}_test")
            default_conn.execute(f"CREATE DATABASE {POSTGRES_DB}_test")

    # create private for testing
    default_engine = create_engine(str(DB_URL), isolation_level="AUTOCOMMIT")
    with default_engine.connect() as default_conn:
        default_conn.execute("CREATE SCHEMA IF NOT EXISTS private")
        default_conn.execute("CREATE SCHEMA IF NOT EXISTS public")
        default_conn.execute("CREATE SCHEMA IF NOT EXISTS users")
        default_conn.execute("CREATE SCHEMA IF NOT EXISTS about")
        default_conn.execute("CREATE SCHEMA IF NOT EXISTS news")
        default_conn.execute("CREATE SCHEMA IF NOT EXISTS subscriptions")
        default_conn.execute("CREATE SCHEMA IF NOT EXISTS history")

    # create private for live db
    if DB_URL != DATABASE_URL:
        default_engine = create_engine(str(DATABASE_URL), isolation_level="AUTOCOMMIT")
        with default_engine.connect() as default_conn:
            default_conn.execute("CREATE SCHEMA IF NOT EXISTS private")

    connectable = config.attributes.get("connection", None)
    config.set_main_option("sqlalchemy.url", DB_URL)

    if connectable is None:
        connectable = engine_from_config(
            config.get_section(config.config_ini_section),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
        )

    with connectable.connect() as connection:
        alembic.context.configure(
            version_table_schema="public",
            connection=connection,
            target_metadata=target_metadata
        )

        with alembic.context.begin_transaction():
            alembic.context.run_migrations()

def run_migrations_offline() -> None:
    """
    Run migrations in 'offline' mode.
    """
    if os.environ.get("TESTING"):
        raise DatabaseError("Running testing migrations offline currently not permitted")

    alembic.context.configure(url=str(DATABASE_URL))

    with alembic.context.begin_transaction():
        alembic.context.run_migrations()

if alembic.context.is_offline_mode():
    logger.info("Running migrations offline")
    run_migrations_offline()
else:
    logger.info("Running migrations online")
    run_migrations_online()
