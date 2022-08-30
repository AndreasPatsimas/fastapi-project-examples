import json
import sys
from fastapi import Depends, APIRouter
import models
from database import get_db
from sqlalchemy.orm import Session

sys.path.append("../..")

router = APIRouter(prefix="/dummy-data", tags=["dummy_data"], responses={204: {"description": "No Content"}})


@router.post("/", status_code=201, response_description="CREATED")
async def populate(db: Session = Depends(get_db)):

    dummy_data = []
    with open("/pagination_api_example/data.json") as file:
        data = json.load(file)

    for d in data:
        dummy_data_model = models.DummyData()
        dummy_data_model.title = d["title"]
        dummy_data_model.completed = d["completed"]
        dummy_data.append(dummy_data_model)

    db.add_all(dummy_data)
    db.commit()
