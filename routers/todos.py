import sys

sys.path.append("..")


from fastapi import Depends, HTTPException, APIRouter
from fastapi.background import BackgroundTasks
import models
import time
from schema import Todo, Dummy
from database import get_db
from sqlalchemy.orm import Session
from .auth import get_current_user, get_user_exception

router = APIRouter(prefix="/todos", tags=["todos"], responses={404: {"description": "Not Found"}})


@router.get("/")
async def read_all(db: Session = Depends(get_db)):
    return db.query(models.Todos).all()


@router.get("/user")
async def read_all_by_user(user: dict = Depends(get_current_user),
                           db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    return db.query(models.Todos)\
        .filter(models.Todos.owner_id == user.get("id"))\
        .all()


@router.get("/{todo_id}")
async def read_todo(todo_id: int,
                    user: dict = Depends(get_current_user),
                    db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    todo_model = db.query(models.Todos)\
        .filter(models.Todos.id == todo_id)\
        .filter(models.Todos.owner_id == user.get("id"))\
        .first()
    if todo_model is not None:
        return todo_model
    raise http_exception()


@router.post("/")
async def create_todo(dummy: Dummy, background_tasks: BackgroundTasks,
                      user: dict = Depends(get_current_user),
                      db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    todo_model = models.Todos()
    todo_model.title = dummy.todo.title
    todo_model.description = dummy.todo.description
    todo_model.priority = dummy.todo.priority
    todo_model.complete = dummy.todo.complete
    todo_model.owner_id = user.get("id")

    db.add(todo_model)
    db.commit()

    data = {
        "title": dummy.title,
        "completed": dummy.completed
    }

    background_tasks.add_task(save_dummy, data, db)

    return successful_response(201)


@router.put("/{todo_id}")
async def update_todo(todo_id: int,
                      todo: Todo,
                      user: dict = Depends(get_current_user),
                      db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()

    todo_model = db.query(models.Todos)\
        .filter(models.Todos.id == todo_id)\
        .filter(models.Todos.owner_id == user.get("id"))\
        .first()

    if todo_model is None:
        raise http_exception()

    todo_model.title = todo.title
    todo_model.description = todo.description
    todo_model.priority = todo.priority
    todo_model.complete = todo.complete

    db.add(todo_model)
    db.commit()

    return successful_response(200)


@router.delete("/{todo_id}")
async def delete_todo(todo_id: int,
                      user: dict = Depends(get_current_user),
                      db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()

    todo_model = db.query(models.Todos)\
        .filter(models.Todos.id == todo_id)\
        .filter(models.Todos.owner_id == user.get("id"))\
        .first()

    if todo_model is None:
        raise http_exception()

    db.query(models.Todos)\
        .filter(models.Todos.id == todo_id)\
        .delete()

    db.commit()

    return successful_response(200)


def successful_response(status_code: int):
    return {
        'status': status_code,
        'transaction': 'Successful'
    }


def http_exception():
    return HTTPException(status_code=404, detail="Todo not found")


def save_dummy(data: dict, db: Session):
    time.sleep(5)
    dummy_data = models.DummyData()
    dummy_data.title = data["title"]
    dummy_data.completed = data["completed"]

    db.add(dummy_data)
    db.commit()

















