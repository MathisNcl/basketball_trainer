from bball_trainer.models import GameRecord

from sqlalchemy.orm import Session

from typing import Any


def save_game_record(db: Session, game_record: GameRecord) -> GameRecord:
    db.add(game_record)
    db.commit()
    db.refresh(game_record)
    return game_record


def create_game_record(db: Session, **kwargs: Any) -> GameRecord:
    game_record = GameRecord(**kwargs)
    return save_game_record(db=db, game_record=game_record)
