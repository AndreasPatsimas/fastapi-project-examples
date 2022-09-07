from pydantic import BaseModel, Field
from typing import Optional, List


class UserModel(BaseModel):
    username: str
    email: Optional[str]
    first_name: str
    last_name: str
    todos: List

    class Config:  # this converts domain to dto
        orm_mode = True


class CreateUser(BaseModel):
    username: str
    email: Optional[str]
    phone_number: str
    first_name: str
    last_name: str
    password: str


class ChangePassword(BaseModel):
    old_password: str
    new_password: str


class Todo(BaseModel):
    title: str
    description: Optional[str]
    priority: int = Field(gt=0, lt=6, description="The priority must be between 1-5")
    complete: bool


class Dummy(BaseModel):
    todo: Todo
    title: str
    completed: bool

class Address(BaseModel):
    address1: str
    address2: Optional[str]
    city: str
    state: str
    country: str
    postalcode: str
    apt_num: Optional[str]


class TransactionRollBackModel(BaseModel):
    address_id: int
    apt_num: str
    dummy_title: str
    completed: bool