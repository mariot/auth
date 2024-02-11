import random
import string

from fastapi import FastAPI, Depends, HTTPException
from app import models, schemas
from sqlalchemy.orm import Session

from app.database import engine, get_db
from app.schemas import UserCreateResponse
from app.service import UserService

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post("/users/", response_model=UserCreateResponse)
def create_user(
    user: schemas.UserCreate, db: Session = Depends(get_db)
) -> UserCreateResponse:
    db_id = UserService.get(db, attributes=["id"], username=user.username)
    if db_id:
        raise HTTPException(status_code=400, detail="Email already registered")
    token = "".join(random.choice(string.ascii_letters) for _ in range(12))
    new_user = UserService.create(db, username=user.username, token=token)
    return UserCreateResponse(token=new_user.token)
