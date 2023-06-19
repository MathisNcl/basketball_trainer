from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class UserBase(BaseModel):
    pseudo: str = Field(min_length=5, max_length=30)

    last_name: str
    first_name: str
    age: Optional[int] = Field(ge=13)


class UserIn(UserBase):
    password: str = Field(min_length=5, max_length=30)


class UserOut(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    last_name: Optional[str]
    first_name: Optional[str]
    age: Optional[int] = Field(ge=13)
    password: Optional[str]


class UserLogin(BaseModel):
    pseudo: str
    password: str


class LoginResult(BaseModel):
    pseudo: str
    connected: bool
