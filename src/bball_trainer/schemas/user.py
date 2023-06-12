from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    pseudo: str

    last_name: str
    first_name: str
    age: Optional[int]


class UserIn(UserBase):
    password: str


class UserOut(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    last_name: Optional[str]
    first_name: Optional[str]
    age: Optional[int]
    password: Optional[str]
