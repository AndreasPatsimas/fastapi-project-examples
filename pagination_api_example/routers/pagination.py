from enum import Enum
from typing import Optional, Tuple, List

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import desc
from pagination_api_example.pagination_service import fetch_data
from database import get_db
import models

from fastapi_pagination import Page, LimitOffsetPage, paginate, add_pagination

router = APIRouter(prefix="/pagination", tags=["pagination"], responses={404: {"description": "Not Found"}})


class SortDirection(str, Enum):
    asc = "ASC"
    desc = "DESC"


class DummyDataModel(BaseModel):
    id: int
    title: str
    completed: bool

    class Config:
        orm_mode = True


class DummyDataSearchCriteria(BaseModel):
    id: Optional[int] = None
    title: Optional[str] = None
    completed: Optional[bool] = None


@router.get("/dummy-data/")
async def find_dummy_data(page_num: int = 1, page_size: int = 10):
    return fetch_data(page_num, page_size)


@router.post("/dummy-data-db/", response_model=Page[DummyDataModel])
@router.post("/dummy-data-db/limit-offset/", response_model=LimitOffsetPage[DummyDataModel])
async def find_dummy_data_db(sort_by: Optional[str] = None, sort_direction: Optional[SortDirection] = None,
                             search_criteria: DummyDataSearchCriteria = None,
                             db: Session = Depends(get_db)):
    criterion = get_criteria(search_criteria)

    if sort_by is None or sort_direction is None:
        return paginate(db.query(models.DummyData).filter(*criterion).all())

    if sort_direction == SortDirection.asc:
        return paginate(db.query(models.DummyData).filter(*criterion).order_by(sort_by).all())

    return paginate(db.query(models.DummyData).filter(*criterion).order_by(desc(sort_by)).all())


def get_criteria(search_criteria: DummyDataSearchCriteria) -> Tuple:
    if search_criteria is None:
        return ()

    criterion = list()
    if search_criteria.id is not None:
        criterion.append(models.DummyData.id == search_criteria.id)
    if search_criteria.title is not None:
        criterion.append(models.DummyData.title.like(f'{search_criteria.title}%'))
    if search_criteria.completed is not None:
        criterion.append(models.DummyData.completed.__eq__(search_criteria.completed))

    return tuple(criterion)


add_pagination(router)
