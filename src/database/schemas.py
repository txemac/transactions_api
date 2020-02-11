from datetime import date
from datetime import datetime
from typing import Dict
from typing import List
from typing import Literal

from pydantic import BaseModel
from pydantic import Field


class UserPost(BaseModel):
    name: str = Field(..., min_length=3, max_length=150)
    email: str = Field(..., min_length=3, max_length=150)
    age: int = Field(..., gt=0)


class UserGet(UserPost):
    id: int = Field(..., gt=0)
    dt_created: datetime

    class Config:
        orm_mode = True


class TransactionPost(BaseModel):
    reference: str = Field(..., min_length=3, max_length=150)
    account: str = Field(..., min_length=3, max_length=150)
    date: date
    amount: float
    type: Literal['inflow', 'outflow']
    category: str = Field(..., min_length=3, max_length=150)


class TransactionGet(TransactionPost):
    id: int = Field(..., gt=0)
    user_id: int = Field(..., gt=0)
    dt_created: datetime

    class Config:
        orm_mode = True


class TransactionPostList(BaseModel):
    name: str
    transactions: List[TransactionPost]


class TransactionSummaryByAccount(BaseModel):
    account: str
    balance: float
    total_inflow: float
    total_outflow: float

    class Config:
        orm_mode = True


class TransactionSummaryByCategory(BaseModel):
    inflow: Dict[str, float]
    outflow: Dict[str, float]

    class Config:
        orm_mode = True
