from typing import Optional

from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime


class Post(SQLModel, table=True):
    id: int = Field(primary_key=True)
    text: str = Field(nullable=False)
    date: datetime = Field(nullable=False, default=datetime.now())
    user_id: int = Field(default=None, nullable=False, foreign_key='user.id')
    user: Optional['User'] = Relationship(back_populates='posts')
