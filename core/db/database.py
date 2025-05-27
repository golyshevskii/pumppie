from collections.abc import AsyncGenerator

from core.db.models.base import Base
from core.settings import settings
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

DB_ENGINE = None
ASESSION = None


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    if ASESSION is None:
        raise RuntimeError("Database is not initialized. Please build the app first.")

    async with ASESSION() as session:
        yield session


def init_db():
    global DB_ENGINE, ASESSION

    DB_ENGINE = create_async_engine(
        url=settings.model_extra["ENV_VAR_DB_URL"],
        echo=settings.SQL_ECHO,
        pool_size=settings.DATABASE_POOL_SIZE,
        max_overflow=settings.DATABASE_MAX_OVERFLOW,
        pool_timeout=settings.DATABASE_POOL_TIMEOUT,
        connect_args=settings.DATABASE_CONNECT_ARGS,
    )

    ASESSION = sessionmaker(
        bind=DB_ENGINE, class_=AsyncSession, expire_on_commit=False, autoflush=False, autocommit=False
    )

    from sqlalchemy import create_engine, text

    engine = create_engine(
        url=settings.model_extra["ENV_VAR_DB_URL"], echo=settings.SQL_ECHO, connect_args=settings.DATABASE_CONNECT_ARGS
    )

    # NOTE: DB must be active
    with engine.connect() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS raw;"))
        conn.commit()

    Base.metadata.create_all(engine)
