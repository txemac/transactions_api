from datetime import date

from database import Transaction
from database import User
from database.schemas import TransactionPost
from database.schemas import TransactionPostList


def test_transaction_create_ok(session, data_transaction):
    count1 = session.query(Transaction).count()
    users = User.get_users(db_session=session)
    data = TransactionPost(
        reference=data_transaction['reference'],
        account=data_transaction['account'],
        date=data_transaction['date'],
        amount=data_transaction['amount'],
        type=data_transaction['type'],
        category=data_transaction['category'],
    )
    Transaction.create(
        db_session=session,
        user_id=users[0].id,
        data=data
    )
    count2 = session.query(Transaction).count()
    assert count1 + 1 == count2


def test_transaction_create_bulk_ok(session, new_user):
    count1 = session.query(Transaction).count()
    data_1 = TransactionPost(
        reference='reference1',
        account='account',
        date=date.today(),
        amount=1.00,
        type='inflow',
        category='category',
    )
    data_2 = TransactionPost(
        reference='reference2',
        account='account',
        date=date.today(),
        amount=1.00,
        type='inflow',
        category='category',
    )
    data = TransactionPostList(transactions=[data_1, data_2])
    Transaction.create_bulk(
        db_session=session,
        user_id=new_user.id,
        transactions=data
    )
    count2 = session.query(Transaction).count()
    assert count1 + 2 == count2


def test_transaction_create_bulk_reference_duplicated(session, new_user):
    count1 = session.query(Transaction).count()
    data_1 = TransactionPost(
        reference='reference1',
        account='account',
        date=date.today(),
        amount=1.00,
        type='inflow',
        category='category',
    )
    data = TransactionPostList(transactions=[data_1, data_1])
    Transaction.create_bulk(
        db_session=session,
        user_id=new_user.id,
        transactions=data
    )
    count2 = session.query(Transaction).count()
    assert count1 + 1 == count2


def test_transaction_get_transaction_by_reference_ok(session, new_transaction):
    assert Transaction.get_transaction_by_reference(db_session=session,
                                                    reference=new_transaction.reference) is not None


def test_transaction_get_transaction_by_reference_not_exists(session):
    assert Transaction.get_transaction_by_reference(db_session=session, reference='not_exists') is None


def test_transaction_get_summary_by_account_empty(session, new_user):
    assert Transaction.get_summary_by_account(db_session=session, user_id=new_user.id) == []


def test_transaction_get_summary_by_account_ok(session, new_user, scenario):
    expected = [
        {
            "account": "C00099",
            "balance": 1738.87,
            "total_inflow": 2500.72,
            "total_outflow": -761.85
        },
        {
            "account": "S00012",
            "balance": 150.72,
            "total_inflow": 150.72,
            "total_outflow": 0.00
        },
    ]
    assert Transaction.get_summary_by_account(db_session=session, user_id=new_user.id) == expected


def test_transaction_get_summary_by_category_empty(session, new_user):
    expected = dict(
        inflow=dict(),
        outflow=dict()
    )
    assert Transaction.get_summary_by_category(db_session=session, user_id=new_user.id) == expected


def test_transaction_get_summary_by_category_ok(session, new_user, scenario):
    expected = {
        "inflow": {
            "salary": 2500.72,
            "savings": 150.72
        },
        "outflow": {
            "groceries": -51.13,
            "rent": -560.00,
            "transfer": -150.72
        }
    }
    assert Transaction.get_summary_by_category(db_session=session, user_id=new_user.id) == expected
