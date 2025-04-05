from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config
from sqlalchemy.engine import Connection
from alembic import context
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from app.db.base import Base  # Импортируйте Base из вашего проекта
from app.core.config import settings  # Импортируйте настройки, где хранится DATABASE_URL
from app.db.base_models import *
from geoalchemy2.admin.dialects.common import _check_spatial_type
from geoalchemy2 import Geometry,Geography, Raster
# Этот объект Alembic Config предоставляет доступ к значениям из файла .ini
config = context.config

# Настройка логирования
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Укажите метаданные ваших моделей для автогенерации миграций
target_metadata = Base.metadata


def render_item(obj_type, obj, autogen_context):
  """Apply custom rendering for selected items."""
  if obj_type == 'type' and isinstance(obj, (Geometry, Geography, Raster)):
    import_name = obj.__class__.__name__
    autogen_context.imports.add(f"from geoalchemy2 import {import_name}")
    return "%r" % obj

  # default rendering for other objects
  return False


def include_object(object, name, type_, reflected, compare_to):
  # Stop making 'index' for geometry column
  if type_ == "index":
    if len(object.expressions) == 1:
      try:
        col = object.expressions[0]
        if (
            _check_spatial_type(col.type, (Geometry, Geography, Raster))
            and col.type.spatial_index
        ):
          return False
      except AttributeError:
        pass
  # Exclude 'spatial_ref_sys' from migrations
  if type_ == "table" and name == "spatial_ref_sys":
    return False

  return True

def run_migrations_offline() -> None:
    """Запуск миграций в 'offline' режиме.

    В этом режиме создается URL подключения, и миграции выполняются без подключения к базе данных.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        include_object=include_object,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    """Выполнение миграций."""
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        render_item=render_item,
        include_object=include_object
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Запуск миграций в 'online' режиме.

    В этом режиме создается асинхронный движок и подключение к базе данных.
    """
    # connectable = async_engine_from_config(
    #   config.get_section(config.config_ini_section),
    #   prefix="sqlalchemy.",
    #   poolclass=pool.NullPool,
    # )
    connectable = create_async_engine(
      settings.DATABASE_URL,  # Используем URL из настроек
      poolclass=pool.NullPool,
    )
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    import asyncio

    asyncio.run(run_migrations_online())