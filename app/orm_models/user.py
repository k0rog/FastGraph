import re
from sqlmodel import SQLModel, Relationship, Field
from pydantic import EmailStr


class PhoneNumber(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(
            pattern=r'^(\+)[1-9][0-9\-\(\)\.]{9,15}$',
            examples=['+375251174895'],
        )

    @classmethod
    def validate(cls, value):
        if not isinstance(value, str):
            raise TypeError('string required')
        regex = r"^(\+)[1-9][0-9\-\(\)\.]{9,15}$"
        if value and not re.search(regex, value, re.I):
            raise ValueError("Phone Number Invalid.")
        return value

    def __repr__(self):
        return f'PhoneNumber({super().__repr__()})'


class User(SQLModel, table=True):
    id: int = Field(primary_key=True)
    email: EmailStr = Field(unique=True)
    first_name: str
    last_name: str
    phone: PhoneNumber = Field(unique=True)
    posts: list['Post'] = Relationship(back_populates='user')

    class Config:
        orm_mode = True
