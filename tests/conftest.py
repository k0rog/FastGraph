import asyncio
import os

import pytest
from sqlalchemy.orm import sessionmaker, scoped_session

from app.repositories.user import UserRepository
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from dotenv import load_dotenv


@pytest.fixture(scope='session')
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
async def settings():
    load_dotenv('.env.test')
    os.environ.setdefault('ENVIRONMENT', 'test')
    from app.core.settings import settings
    return settings


# @pytest.fixture(scope='session')
# def app():
#     app = create_app(dotenv_filename='.env.test')
#     app.config.update({
#         'TESTING': True,
#     })
#
#     with app.app_context():
#         yield app
#
#

@pytest.fixture(scope='session')
async def connection(settings):
    from app.orm_models import user
    from app.orm_models import post
    engine = create_async_engine(settings.DATABASE_URL)

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


# @pytest.fixture(scope='function')
# def client(app, storage):
#     client = app.test_client()
#
#     yield client


@pytest.fixture(scope='function')
async def user_repository(session) -> UserRepository:
    repository = UserRepository(
        session=session,
    )

    yield repository


# @pytest.fixture(scope='session')
# def permanent_session(db):
#     session = db.session
#     yield session
#     session.close()
#
#
# @pytest.fixture(scope='session')
# def bank_account(permanent_session):
#     while True:
#         try:
#             bank_account = BankAccount(
#                 currency='BYN',
#                 balance=0,
#             )
#
#             permanent_session.add(bank_account)
#             permanent_session.commit()
#
#             break
#         except IntegrityError:
#             '''There's very small chance to generate duplicated IBAN
#             But since this chance still exists, we have to repeat the operation'''
#             permanent_session.rollback()
#
#     association_row = AssociationBankAccountCustomer(
#         bank_account_id=bank_account.IBAN,
#         customer_id='MockUUID'
#     )
#
#     permanent_session.add(association_row)
#     permanent_session.commit()
#
#     yield bank_account
#
#
# @pytest.fixture(scope='session')
# def customer(permanent_session):
#     customer = Customer(
#         first_name='John',
#         last_name='Smith',
#         email='jsmith@gmail.com',
#         passport_number='HB1111111',
#     )
#
#     permanent_session.add(customer)
#     permanent_session.commit()
#
#     yield customer
