from datetime import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bball_trainer.models import Base, User


class GameRecord(Base):
    score: Mapped[int]
    user_id = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(uselist=False, cascade="all,delete", backref="parent")
    created_at: Mapped[datetime] = mapped_column(default=func.now())
