import sys

sys.path.append("..")

from fastapi import Depends, HTTPException, APIRouter
import models
from database import get_db
from sqlalchemy.orm import Session
from schema import TransactionRollBackModel

router = APIRouter(prefix="/transactions", tags=["transactions"], responses={204: {"description": "No Content"}})


@router.put("/", status_code=202, response_description="ACCEPTED")
async def update(transaction_model: TransactionRollBackModel,
                 db: Session = Depends(get_db)):
    try:
        address = db.query(models.Address).filter(models.Address.id == transaction_model.address_id).first()
        address.apt_num = transaction_model.apt_num
        db.add(address)

        dummy_data = models.DummyData()
        dummy_data.title = transaction_model.dummy_title
        dummy_data.completed = transaction_model.completed
        db.add(dummy_data)

        db.commit()

    except:
        db.rollback()
        raise HTTPException(status_code=204, detail="Transaction not completed")
