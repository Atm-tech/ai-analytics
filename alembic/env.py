import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

from dotenv import load_dotenv
load_dotenv()

# 🔧 Add the project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# ✅ Import your model's metadata
from app.models.product import Base  # Add more models as needed
from app.models.purchase import Base
from app.models.stock import Base
from app.models.sale import Base
from app.models.outlet import Base
from app.models.speed_tier_definition import Base
from app.models.definition_set import Base
from app.models.definition import Base
# Alembic Config
config = context.config

# Set up logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 🌍 Determine environment
ENV = os.getenv("ENV", "dev")

# Load DB URL from .env
if ENV == "prod":
    db_url = os.getenv("POSTGRES_DB_URL")
else:
    db_url = os.getenv("LOCAL_DB_URL", "sqlite:///./isms.db")

# Inject DB URL into Alembic config
config.set_main_option("sqlalchemy.url", db_url)

# Provide metadata for autogenerate support
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations without a DB connection."""
    context.configure(
        url=db_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations using a live DB connection."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
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
