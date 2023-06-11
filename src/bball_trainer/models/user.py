from typing import Optional

from sqlalchemy.orm import Mapped
from werkzeug.security import check_password_hash, generate_password_hash

from bball_trainer.models import Base


class User(Base):
    pseudo: Mapped[str]
    password_hash: Mapped[str]

    last_name: Mapped[str]
    first_name: Mapped[str]
    age: Mapped[Optional[int]]

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)
