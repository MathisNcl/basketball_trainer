from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, validator


class GameRecordBase(BaseModel):
    score: int
    user_id: int
    difficulty: str
    time: int
    point_per_sec: Optional[float]

    @validator("point_per_sec", always=True)
    def compute_point_per_second(cls, v: Optional[str], values: dict[str, Any]) -> float:
        time = values.get("time")
        if time is None:
            return 0
        return round(values.get("score", 0) / time, 3)


class GameRecordIn(GameRecordBase):
    pass


class GameRecordOut(GameRecordBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
