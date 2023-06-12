from typing import Generator, List, Optional

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from bball_trainer import __version__ as version
from bball_trainer import models
from bball_trainer.crud import game_record as crud_gr
from bball_trainer.crud import user as crud_user
from bball_trainer.models.database import SessionFactory, engine
from bball_trainer.schemas import GameRecordIn, GameRecordOut, UserIn, UserOut, UserUpdate

app = FastAPI(
    title="Basketball trainer API",
    description="This API is used to create, retrieve, update and removed backend data for the basket ball trainer app",
    version=version,
)
models.Base.metadata.create_all(bind=engine)


# Dependency
def get_db() -> Generator:
    db = SessionFactory()
    try:
        yield db
    finally:
        db.close()


# User
@app.get(
    "/user/", response_model=Optional[List[UserOut]], description="Récupération de tous les utilisateur", tags=["user"]
)
async def get_all_users(db: Session = Depends(get_db)) -> Optional[List[models.User]]:
    all_users: Optional[List[models.User]] = crud_user.get_all_users(db)
    return all_users


@app.get("/user/{user_id}", response_model=UserOut, description="Récupération d'un utilisateur", tags=["user"])
async def get_user(user_id: int, db: Session = Depends(get_db)) -> Optional[models.User]:
    db_user: Optional[models.User] = crud_user.get_user(db, id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail=f"{user_id} is not a known id.")
    return db_user


@app.post(
    "/user/",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
    description="Création d'un utilisateur",
    tags=["user"],
)
async def create_user(user_in: UserIn, db: Session = Depends(get_db)) -> models.User:
    user_saved: models.User = crud_user.create_user(db, **user_in.dict())
    return user_saved


@app.patch(
    "/user/{user_id}",
    response_model=UserOut,
    status_code=status.HTTP_200_OK,
    description="Mise à jour d'un utilisateur",
    tags=["user"],
)
async def update_user(user_id: int, user_in: UserUpdate, db: Session = Depends(get_db)) -> models.User:
    db_user: Optional[models.User] = crud_user.get_user(db, id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail=f"{user_id} is not a known id.")
    db_user = crud_user.update_user(db=db, user=db_user, data=user_in.dict(exclude_unset=True))
    return db_user


@app.delete(
    "/user/{user_id}", status_code=status.HTTP_204_NO_CONTENT, description="Suppression d'un utilisateur", tags=["user"]
)
async def delete_user(user_id: int, db: Session = Depends(get_db)) -> None:
    db_user: Optional[models.User] = crud_user.get_user(db, id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail=f"{user_id} is not a known id.")
    crud_user.delete_user(db, db_user)


# Game Record
@app.post(
    "/game_record/",
    response_model=GameRecordOut,
    status_code=status.HTTP_201_CREATED,
    description="Création d'une partie",
    tags=["game_record"],
)
async def create_game_record(game_record_in: GameRecordIn, db: Session = Depends(get_db)) -> models.GameRecord:
    db_user: Optional[models.User] = crud_user.get_user(db, id=game_record_in.user_id)
    if not db_user:
        raise HTTPException(
            status_code=404, detail=f"{game_record_in.user_id} is not a known id, you can not create a game for it."
        )
    game_saved: models.GameRecord = crud_gr.create_game_record(db, **game_record_in.dict())
    return game_saved


@app.get(
    "/game_record/{user_id}",
    response_model=Optional[List[GameRecordOut]],
    description="Récupération de toutes les parties d'un joueur",
    tags=["game_record"],
)
async def get_all_games_user(user_id: int, db: Session = Depends(get_db)) -> Optional[List[models.GameRecord]]:
    db_user: Optional[models.User] = crud_user.get_user(db, id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail=f"{user_id} is not a known id.")
    db_games: Optional[List[models.GameRecord]] = crud_gr.get_all_games_user(db=db, user_id=user_id)
    return db_games
