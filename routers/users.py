import sys

sys.path.append("..")

from typing import List
from fastapi import Depends, HTTPException, APIRouter, Query
import models
from schema import UserModel, ChangePassword
from database import get_db
from sqlalchemy.orm import Session
import time

from .auth import get_current_user, get_user_exception, get_password_hash, verify_password

router = APIRouter(prefix="/users", tags=["users"], responses={404: {"description": "Not Found"}})


async def time_consuming_test():
    time.sleep(5)
    return 'ok'

@router.get("/", response_model=List[UserModel])
async def all_users(db: Session = Depends(get_db)):
    # await time_consuming_test()  # go ahead and do the rest functionality until complete this task
    return db.query(models.Users).all()


@router.get("/{user_id}", response_model=UserModel)
async def find_by_id(user_id: str, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


'''
Query, Path, Body there are for metadata to describe parameters, also used for data validation like number length etc

alias convert name of json key in the client side
'''
@router.get("/email/", response_model=UserModel)
async def find_by_email(email: str = Query("example@mail.com", title="User email", description="bla bla", alias="mail"),
                        db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.email == email).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/", status_code=202, response_description="ACCEPTED")
async def update(change_password: ChangePassword,
                 logged_user: dict = Depends(get_current_user),
                 db: Session = Depends(get_db)):
    if logged_user is None:
        raise get_user_exception()

    user = db.query(models.Users).filter(models.Users.username == logged_user.get("username")).first()

    if not verify_password(change_password.old_password, user.hashed_password):
        raise HTTPException(status_code=403, detail="Give correct password")

    user.hashed_password = get_password_hash(change_password.new_password)
    db.add(user)
    db.commit()


@router.delete("/", status_code=204)
async def delete_user(logged_user: dict = Depends(get_current_user),
                      db: Session = Depends(get_db)):
    if logged_user is None:
        raise get_user_exception()

    user = db.query(models.Users).filter(models.Users.username == logged_user.get("username")).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db.query(models.Todos) \
        .filter(models.Todos.owner_id == user.id) \
        .delete()

    db.query(models.Users) \
        .filter(models.Users.username == user.username) \
        .delete()

    db.commit()
