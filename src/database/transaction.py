from collections import defaultdict
from datetime import date
from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import func
from sqlalchemy.orm import Session

import database
from database.schemas import TransactionPost
from database.schemas import TransactionPostList


class Transaction(database.Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    reference = Column(String, unique=True, index=True, nullable=False)
    account = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    amount = Column(Float, nullable=False)
    type = Column(String, nullable=False)
    category = Column(String, nullable=False)
    dt_created = Column(DateTime, default=func.now(), nullable=False)

    def __init__(
            self,
            user_id: int,
            reference: str,
            account: str,
            date: datetime.date,
            amount: float,
            type: str,
            category: str,
    ):
        self.user_id = user_id
        self.reference = reference
        self.account = account
        self.date = date
        self.amount = amount
        self.type = type
        self.category = category

    @classmethod
    def create(
            cls,
            db_session: Session,
            user_id: int,
            data: TransactionPost
    ):
        """
        Create a new transaction.

        :param Session db_session: database session
        :param int user_id: ID of the user
        :param TransactionPost data: data
        :return Transaction: transaction
        """
        transaction = Transaction(
            user_id=user_id,
            reference=data.reference,
            account=data.account,
            date=data.date,
            amount=data.amount,
            type=data.type,
            category=data.category,
        )
        db_session.add(transaction)
        db_session.commit()
        db_session.refresh(transaction)

        return transaction

    @classmethod
    def create_bulk(
            cls,
            db_session: Session,
            user_id: int,
            transactions: TransactionPostList,
    ):
        """
        Create transactions in bulk.
        The transactions with references duplicate will not add.

        :param Session db_session: database session
        :param int user_id: ID of the user
        :param list transactions: list of transactions
        :return List: list of transactions
        """
        result = []
        for t in transactions.transactions:
            if Transaction.get_transaction_by_reference(db_session=db_session, reference=t.reference) is None:
                transaction = TransactionPost(
                    reference=t.reference,
                    account=t.account,
                    date=t.date,
                    amount=t.amount,
                    type=t.type,
                    category=t.category,
                )
                t = Transaction.create(
                    db_session=db_session,
                    user_id=user_id,
                    data=transaction,
                )
                result.append(t)

        return result

    @classmethod
    def get_transaction_by_reference(
            cls,
            db_session: Session,
            reference: str,
    ):
        """
        Get a transaction by reference.

        :param Session db_session: database session
        :param str reference: reference
        :return Transaction: transaction
        """
        return db_session.query(cls).filter(cls.reference == reference).first()

    @classmethod
    def get_transaction_by_user_id_date_range(
            cls,
            db_session: Session,
            user_id: int,
            start_date: date = None,
            end_date: date = None,
    ):
        """
        Get transactions by user and with filters by date range.

        :param Session db_session: database session
        :param int user_id: ID of the user
        :param date start_date: filter date start
        :param date end_date: filter date end
        :return list: list of transactions
        """
        query = db_session.query(cls).filter(cls.user_id == user_id)

        if start_date is not None:
            query = query.filter(cls.date >= start_date)

        if end_date is not None:
            query = query.filter(cls.date <= end_date)

        return query.all()

    @classmethod
    def get_summary_by_account(
            cls,
            db_session: Session,
            user_id: int,
            start_date: date = None,
            end_date: date = None,
    ):
        """
        Get the summary by accounts of all user's transactions.

        :param Session db_session: database session
        :param int user_id: id of the user
        :param date start_date: filter start date
        :param date end_date: filter end date
        :return list: references
        """
        transactions = Transaction.get_transaction_by_user_id_date_range(
            db_session=db_session,
            user_id=user_id,
            start_date=start_date,
            end_date=end_date
        )

        result = []
        for transaction in transactions:
            element = next((item for item in result if item['account'] == transaction.account), None)
            if element is None:
                element = dict(
                    account=transaction.account,
                    balance=0.0,
                    total_inflow=0.0,
                    total_outflow=0.0,
                )
                result.append(element)
            element['balance'] += transaction.amount
            if transaction.amount > 0:
                element['total_inflow'] += transaction.amount
            elif transaction.amount < 0:
                element['total_outflow'] += transaction.amount

        return result

    @classmethod
    def get_summary_by_category(
            cls,
            db_session: Session,
            user_id: int,
            start_date: date = None,
            end_date: date = None,
    ):
        """
        Get the summary by category of all user's transactions.

        :param Session db_session: database session
        :param int user_id: id of the user
        :param date start_date: filter start date
        :param date end_date: filter end date
        :return list: references
        """
        transactions = Transaction.get_transaction_by_user_id_date_range(
            db_session=db_session,
            user_id=user_id,
            start_date=start_date,
            end_date=end_date
        )

        result = dict(
            inflow=defaultdict(float),
            outflow=defaultdict(float),
        )

        for transaction in transactions:
            result[transaction.type][transaction.category] += transaction.amount

        return result
