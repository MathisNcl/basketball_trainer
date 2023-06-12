from datetime import datetime

from pydantic import BaseModel


class GameRecordBase(BaseModel):
    score: int
    user_id: int


class GameRecordIn(GameRecordBase):
    pass


class GameRecordOut(GameRecordBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
