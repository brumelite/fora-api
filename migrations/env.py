from alembic import context
from sqlalchemy import engine_from_config, pool
from app.db import Base
from app import models  # noqa
import os
config = context.config
target_metadata = Base.metadata

def run_migrations_online():
    from sqlalchemy import create_engine
    engine = create_engine(os.environ["DATABASE_URL"], poolclass=pool.NullPool)
    with engine.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()
    engine.dispose()

run_migrations_online()
