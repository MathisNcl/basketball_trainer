from bball_trainer.models import User

from sqlalchemy.orm import Session
from sqlalchemy import Select

from typing import Any


def save_user(db: Session, user: User) -> User:
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def create_user(db: Session, **kwargs: Any) -> User:
    user = User(**kwargs)
    return save_user(db=db, user=user)


def update_user(db: Session, user: User, data: dict[str, Any]) -> User:
    for field, value in data.items():
        setattr(user, field, value)
    return save_user(db=db, user=user)


def get_user(db: Session, id: int) -> User:
    return db.scalar(Select(User).filter(User.id == id).first())
