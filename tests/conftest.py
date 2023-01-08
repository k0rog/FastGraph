import asyncio
from testing.postgresql import Postgresql
import pytest
from sqlalchemy.orm import sessionmaker, scoped_session

from app.repositories.user import UserRepository
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine


@pytest.fixture(scope='session')
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
async def connection():
    from app.orm_models import user
    from app.orm_models import post
    with Postgresql() as in_memory_postgres:
        dsn = in_memory_postgres.dsn()
        database_url = 'postgresql+asyncpg://{}@{}:{}/{}'.format(
            dsn['user'], dsn['host'], dsn['port'], dsn['database']
        )
        engine = create_async_engine(database_url)

        connection = await engine.connect()
        await connection.run_sync(SQLModel.metadata.create_all)
        await connection.commit()

        yield connection

        await connection.run_sync(SQLModel.metadata.drop_all)
        await connection.commit()

        await connection.close()
        engine.clear_compiled_cache()


@pytest.fixture(scope='function')
async def session(connection):
    trans = await connection.begin()
    session = scoped_session(
        sessionmaker(
            connection, class_=AsyncSession, expire_on_commit=False
        )
    )

    yield session
    await trans.rollback()


@pytest.fixture(scope='function')
async def user_repository(session) -> UserRepository:
    repository = UserRepository(
        session=session,
    )

    yield repository
