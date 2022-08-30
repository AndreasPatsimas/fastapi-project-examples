import sys
sys.path.append("..")

from fastapi import Depends, APIRouter
import models
from schema import Address
from exceptions import AddressException
from database import get_db
from sqlalchemy.orm import Session
from .auth import get_current_user, get_user_exception

router = APIRouter(
    prefix="/address",
    tags=["address"],
    responses={404: {"description": "Not found"}}
)


@router.post("/")
async def create_address(address: Address,
                         user: dict = Depends(get_current_user),
                         db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()

    if address.address1.startswith("Papanastasiou"):
        raise AddressException("Only Aris!")

    address_model = models.Address()
    address_model.address1 = address.address1
    address_model.address2 = address.address2
    address_model.city = address.city
    address_model.state = address.state
    address_model.country = address.country
    address_model.postalcode = address.postalcode
    address_model.apt_num = address.apt_num

    db.add(address_model)
    db.flush()

    user_model = db.query(models.Users).filter(models.Users.id == user.get("id")).first()

    user_model.address_id = address_model.id

    db.add(user_model)

    db.commit()








