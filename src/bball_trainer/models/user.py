from sqlalchemy.orm import Mapped, mapped_column
from bball_trainer.models import Base
from typing import Optional

from werkzeug.security import generate_password_hash, check_password_hash


class User(Base):
    pseudo: Mapped[str] = mapped_column(primary_key=True)
    password_hash: Mapped[str]

    last_name: Mapped[str]
    first_name: Mapped[str]
    age: Mapped[Optional[int]]

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
