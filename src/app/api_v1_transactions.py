from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette.status import HTTP_200_OK
from starlette.status import HTTP_201_CREATED
from starlette.status import HTTP_400_BAD_REQUEST

from app import messages
from app.utils import check_amounts
from app.utils import check_references
from database import Transaction
from database import get_db
from database.schemas import TransactionGet
from database.schemas import TransactionPostList
from database.schemas import TransactionSummaryByAccount
from database.schemas import TransactionSummaryByCategory

api_v1_transactions = APIRouter()


@api_v1_transactions.post('/{user_id}', response_model=List[TransactionGet], status_code=HTTP_201_CREATED)
def post_transactions(
        *,
        db_session: Session = Depends(get_db),
        user_id: int,
        data: TransactionPostList
) -> List[TransactionGet]:
    if not check_references(transactions=data):
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=messages.TRANSACTIONS_REFERENCES_ERROR)

    if not check_amounts(transactions=data):
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=messages.TRANSACTIONS_AMOUNTS_ERROR)

    return Transaction.create_bulk(db_session=db_session, user_id=user_id, transactions=data)


@api_v1_transactions.get('/{user_id}/summary_by_account', response_model=List[TransactionSummaryByAccount],
                         status_code=HTTP_200_OK)
def get_summary_by_account(
        *,
        db_session: Session = Depends(get_db),
        user_id: int
) -> TransactionSummaryByAccount:
    return Transaction.get_summary_by_account(db_session=db_session, user_id=user_id)


@api_v1_transactions.get('/{user_id}/summary_by_category', response_model=TransactionSummaryByCategory,
                         status_code=HTTP_200_OK)
def get_summary_by_category(
        *,
        db_session: Session = Depends(get_db),
        user_id: int
) -> TransactionSummaryByCategory:
    return Transaction.get_summary_by_category(db_session=db_session, user_id=user_id)
