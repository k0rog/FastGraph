import pytest
from sqlmodel import select
from app.orm_models.user import User
from sqlalchemy.exc import IntegrityError


USER_DATA = {
    'first_name': 'John',
    'last_name': 'Smith',
    'email': 'jsmith@gmail.com',
    'phone': '+375255161732',
}


class TestCreate:
    async def test_is_id_returned(self, user_repository):
        customer = await user_repository.create_user(**USER_DATA)

        assert hasattr(customer, 'id')

    async def test_create(self, user_repository, session):
        await user_repository.create_user(**USER_DATA)

        result = await session.execute(
            select(User).where(User.email == USER_DATA['email'])
        )

        user = result.scalars().first()

        assert user is not None

        assert user.first_name == USER_DATA['first_name']
        assert user.last_name == USER_DATA['last_name']
        assert user.email == USER_DATA['email']
        assert user.phone == USER_DATA['phone']

    async def test_for_duplicated_data(self, user_repository):
        await user_repository.create_user(**USER_DATA)

        with pytest.raises(IntegrityError) as exception_info:
            await user_repository.create_user(**USER_DATA)

#
# class TestIsExists:
#     def test_is_exists_true(self, customer_repository):
#         customer = customer_repository.create(CUSTOMER_DATA)
#
#         assert customer_repository.is_exists(customer.uuid)
#
#     def test_is_exists_false(self, customer_repository):
#         assert not customer_repository.is_exists('NonexistentUUID')
#
#
# class TestUpdate:
#     def test_for_one_field(self, customer_repository, storage):
#         customer = customer_repository.create(CUSTOMER_DATA)
#
#         update_data = {
#             'first_name': 'Bob'
#         }
#
#         customer_repository.update(customer.uuid, update_data)
#
#         storage_customer = storage.session.query(
#             Customer
#         ).filter_by(uuid=customer.uuid).first()
#
#         assert storage_customer.first_name == update_data['first_name']
#
#     def test_for_many_fields(self, customer_repository, storage):
#         customer = customer_repository.create(CUSTOMER_DATA)
#
#         update_data = {
#             'first_name': 'Bob',
#             'last_name': 'Miller'
#         }
#
#         customer_repository.update(customer.uuid, update_data)
#
#         storage_customer = storage.session.query(
#             Customer
#         ).filter_by(uuid=customer.uuid).first()
#
#         assert storage_customer.first_name == update_data['first_name']
#         assert storage_customer.last_name == update_data['last_name']
#
#     def test_for_duplicated_passport_number(self, customer_repository):
#         customer_repository.create(CUSTOMER_DATA)
#
#         second_customer_data = CUSTOMER_DATA.copy()
#         second_customer_data.update({'passport_number': 'HB1111112'})
#
#         second_customer = customer_repository.create(second_customer_data)
#
#         update_data = {
#             'passport_number': CUSTOMER_DATA['passport_number']
#         }
#
#         with pytest.raises(AlreadyExistException) as exception_info:
#             customer_repository.update(second_customer.uuid, update_data)
#
#         assert exception_info.value.message == 'Customer already exist!'
#
#
# class TestDelete:
#     def test_delete(self, customer_repository, storage):
#         customer = customer_repository.create(CUSTOMER_DATA)
#
#         is_deleted = customer_repository.delete(customer.uuid)
#
#         assert is_deleted
#
#         assert storage.session.query(
#             Customer
#         ).filter_by(uuid=customer.uuid).first() is None
#
#     def test_for_nonexistent_customer(self, customer_repository):
#         is_deleted = customer_repository.delete('NonexistentUUID')
#
#         assert not is_deleted
#
#
# class TestGetByUUID:
#     def test_get_by_uuid(self, customer_repository, storage):
#         customer = customer_repository.create(CUSTOMER_DATA)
#
#         retrieved_customer = customer_repository.get_by_uuid(customer.uuid)
#
#         storage_customer = storage.session.query(
#             Customer
#         ).filter_by(uuid=customer.uuid).first()
#
#         assert storage_customer.first_name == retrieved_customer.first_name
#         assert storage_customer.last_name == retrieved_customer.last_name
#         assert storage_customer.email == retrieved_customer.email
#         assert storage_customer.passport_number == retrieved_customer.passport_number
#
#     def test_for_nonexistent_customer(self, customer_repository):
#         with pytest.raises(DoesNotExistException) as exception_info:
#             customer_repository.get_by_uuid('NonexistentUUID')
#
#         assert exception_info.value.message == 'Customer does not exist!'
