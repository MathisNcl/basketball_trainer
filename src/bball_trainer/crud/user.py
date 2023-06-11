from typing import Any

from sqlalchemy import Select
from sqlalchemy.orm import Session

from bball_trainer.models import User


def save_user(db: Session, user: User) -> User:
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def create_user(db: Session, **kwargs: Any) -> User:
    user: User = User(**kwargs)
    user.set_password(user.password_hash)
    return save_user(db=db, user=user)


def update_user(db: Session, user: User, data: dict[str, Any]) -> User:
    for field, value in data.items():
        setattr(user, field, value)
    return save_user(db=db, user=user)


def get_user(db: Session, id: int) -> User:
    return db.scalars(Select(User).filter(User.id == id)).first()
