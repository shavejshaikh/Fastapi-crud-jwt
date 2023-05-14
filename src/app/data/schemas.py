from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional
from typing import Union


class User(BaseModel):
    name : str
    email: str
    password: str


class UserOut(BaseModel):
    # id : int
    name: str
    email : str
    # password: str
    added_on : Optional[date] = None
    update_on : Optional[date] = None

    class Config():
        orm_mode = True


class Login(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type : str


class UserUpdate(BaseModel):
    name : Union[str , None] = None
    email: Union[str , None] = None