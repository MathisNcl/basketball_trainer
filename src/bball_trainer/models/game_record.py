from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, func, Constraint
from bball_trainer.models import Base, User
from datetime import datetime


class GameRecord(Base):
    score: Mapped[int]
    user_id = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(uselist=False)
    created_at: Mapped[datetime] = mapped_column(default=func.now())
