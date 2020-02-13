from datetime import date
from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette.status import HTTP_200_OK
from starlette.status import HTTP_201_CREATED
from starlette.status import HTTP_404_NOT_FOUND

from app import messages
from database import Transaction
from database import User
from database import get_db
from database.schemas import TransactionGet
from database.schemas import TransactionPostList
from database.schemas import TransactionSummaryByAccount
from database.schemas import TransactionSummaryByCategory

api_v1_transactions = APIRouter()


@api_v1_transactions.post('/', response_model=List[TransactionGet], status_code=HTTP_201_CREATED)
def post_transactions(
        *,
        db_session: Session = Depends(get_db),
        payload: TransactionPostList
) -> List[TransactionGet]:
    user = User.get_user_by_name(db_session=db_session, name=payload.name)
    if user is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=messages.USER_NOT_FOUND)

    data = []
    references_db = Transaction.get_referencez(db_session=db_session)
    for transaction in payload.transactions:
        if transaction.reference not in references_db:
            transaction.user_id = user.id
            references_db.append(transaction.reference)
            data.append(dict(transaction))

    return Transaction.create_bulk(
        db_session=db_session,
        data=data
    )


@api_v1_transactions.get('/summary_by_account', response_model=List[TransactionSummaryByAccount],
                         status_code=HTTP_200_OK)
def get_summary_by_account(
        *,
        db_session: Session = Depends(get_db),
        name: str,
        start_date: date = None,
        end_date: date = None,
) -> TransactionSummaryByAccount:
    user = User.get_user_by_name(db_session=db_session, name=name)
    if user is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=messages.USER_NOT_FOUND)

    return Transaction.get_summary_by_account(
        db_session=db_session,
        user_id=user.id,
        start_date=start_date,
        end_date=end_date
    )


@api_v1_transactions.get('/summary_by_category', response_model=TransactionSummaryByCategory,
                         status_code=HTTP_200_OK)
def get_summary_by_category(
        *,
        db_session: Session = Depends(get_db),
        name: str,
        start_date: date = None,
        end_date: date = None,
) -> TransactionSummaryByCategory:
    user = User.get_user_by_name(db_session=db_session, name=name)
    if user is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=messages.USER_NOT_FOUND)

    return Transaction.get_summary_by_category(
        db_session=db_session,
        user_id=user.id,
        start_date=start_date,
        end_date=end_date
    )
