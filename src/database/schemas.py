from datetime import date
from datetime import datetime
from typing import Dict
from typing import List
from typing import Literal

from pydantic import BaseModel
from pydantic import Field
from pydantic import validator

from app import messages


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
    user_id: int = None
    reference: str = Field(..., min_length=3, max_length=150)
    account: str = Field(..., min_length=3, max_length=150)
    date: date
    type: Literal['inflow', 'outflow']
    amount: float
    category: str = Field(..., min_length=3, max_length=150)

    @validator('amount')
    def amount_positive_negative(cls, v, values):
        if ('type' in values and values['type'] == 'inflow' and v < 0) or \
                ('type' in values and values['type'] == 'outflow' and v > 0):
            raise ValueError(messages.TRANSACTIONS_AMOUNTS_ERROR)
        return v

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
