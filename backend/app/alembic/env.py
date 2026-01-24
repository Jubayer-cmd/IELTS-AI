"""
Alembic migration environment.

Configured for SQLModel with async support if needed.
"""
from logging.config import fileConfig

from sqlalchemy import pool
from sqlmodel import SQLModel

from alembic import context

# Import all models to ensure they're registered with SQLModel.metadata
from app.models.users import User  # noqa: F401
# from app.models.essay import Essay  # Add when you create Essay model
from app.core.config import settings

# Alembic Config object
config = context.config

# Override sqlalchemy.url with our settings
config.set_main_option("sqlalchemy.url", str(settings.DATABASE_URL))

# Logging configuration
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata for autogenerate
target_metadata = SQLModel.metadata


def run_migrations_offline() -> None:
    """
    Run migrations in 'offline' mode.

    This configures the context with just a URL and not an Engine.
    Calls to context.execute() emit the given SQL to the script output.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """
    Run migrations in 'online' mode.

    Creates an Engine and associates a connection with the context.
    """
    from sqlalchemy import create_engine

    connectable = create_engine(
        config.get_main_option("sqlalchemy.url"),
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
