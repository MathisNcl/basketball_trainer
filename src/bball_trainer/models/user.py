from datetime import datetime
from typing import Optional

from sqlalchemy import func, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from werkzeug.security import check_password_hash, generate_password_hash

from bball_trainer.models import Base


class User(Base):
    pseudo: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]

    last_name: Mapped[str]
    first_name: Mapped[str]
    age: Mapped[Optional[int]]

    created_at: Mapped[datetime] = mapped_column(default=func.now())

    def set_password(self, password: str) -> None:
        self.password = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)
