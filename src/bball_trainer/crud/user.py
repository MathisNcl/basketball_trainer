from typing import Any, List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from bball_trainer.models import User


def save_user(db: Session, user: User) -> User:
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def create_user(db: Session, **kwargs: Any) -> User:
    user: User = User(**kwargs)
    user.set_password(user.password)
    return save_user(db=db, user=user)


def update_user(db: Session, user: User, data: dict[str, Any]) -> User:
    for field, value in data.items():
        if field == "password":
            user.set_password(password=value)
        else:
            setattr(user, field, value)
    return save_user(db=db, user=user)


def get_user(db: Session, id: int) -> Optional[User]:
    return db.scalars(select(User).filter(User.id == id)).first()


def get_all_users(db: Session) -> List[User]:
    return db.scalars(select(User)).all()  # type: ignore


def delete_user(db: Session, user_db: User) -> None:
    db.delete(user_db)
    db.commit()
