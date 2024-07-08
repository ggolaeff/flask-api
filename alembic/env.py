from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# Импортируем Base из вашего модуля моделей
from models import Base

# Указываем метаданные
target_metadata = Base.metadata

# Alembic Config объект, который предоставляет доступ к значениям внутри .ini файла
config = context.config

# Интерпретируем config файл для Python логгирования.
# Эта строка в основном настраивает логгеры.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# другие значения из конфигурации, определенные нуждами env.py,
# могут быть получены здесь:
# my_important_option = config.get_main_option("my_important_option")
# ... и так далее.


def run_migrations_offline() -> None:
    """Запуск миграций в 'offline' режиме.

    Это настраивает контекст только с URL
    и без Engine, хотя Engine также допустим.
    Пропуская создание Engine, нам даже не нужен DBAPI.

    Вызовы context.execute() здесь испускают данную строку на
    выход скрипта.

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
    """Запуск миграций в 'online' режиме.

    В этом сценарии нам нужно создать Engine
    и ассоциировать подключение с контекстом.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
