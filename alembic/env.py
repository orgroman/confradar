from __future__ import annotations

import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# Ensure the package path is available when running from repo root
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
PKG_SRC = os.path.join(ROOT, "packages", "confradar", "src")
if PKG_SRC not in sys.path:
    sys.path.insert(0, PKG_SRC)

target_metadata = None

try:
    from confradar.db.base import Base  # type: ignore
    target_metadata = Base.metadata
except Exception:
    target_metadata = None

# Interpret the config file for Python logging.
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


def get_url() -> str:
    # Prefer DATABASE_URL environment variable
    url = os.getenv("DATABASE_URL")
    if url:
        return url
    # Fallback to package settings if available
    try:
        from confradar.settings import settings  # type: ignore

        return settings.database_url
    except Exception:
        return "sqlite:///confradar.db"


def run_migrations_offline() -> None:
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    configuration = config.get_section(config.config_ini_section) or {}
    configuration["sqlalchemy.url"] = get_url()

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
