from typing import Any, List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from bball_trainer.models import GameRecord


def save_game_record(db: Session, game_record: GameRecord) -> GameRecord:
    db.add(game_record)
    db.commit()
    db.refresh(game_record)
    return game_record


def create_game_record(db: Session, **kwargs: Any) -> GameRecord:
    game_record = GameRecord(**kwargs)
    return save_game_record(db=db, game_record=game_record)


def get_game(db: Session, id: int) -> Optional[GameRecord]:
    return db.scalars(select(GameRecord).filter(GameRecord.id == id)).first()


def get_all_games_user(db: Session, user_id: int) -> List[GameRecord]:
    return db.scalars(select(GameRecord).filter(GameRecord.user_id == user_id)).all()  # type: ignore


def get_top_nb_pps(db: Session, nb: int) -> List[GameRecord]:
    return db.scalars(select(GameRecord).order_by(GameRecord.point_per_sec.desc()).limit(nb)).all()  # type: ignore
