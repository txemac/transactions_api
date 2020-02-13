import os

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy_utils import create_database
from sqlalchemy_utils import database_exists
from sqlalchemy_utils import drop_database
from starlette.testclient import TestClient

from app.main import app
from database import Base
from database import Transaction
from database import User
from database import get_db
from database.schemas import TransactionPost
from database.schemas import UserPost

url = f'{os.getenv("DATABASE_URL")}_test'
_db_conn = create_engine(url)


def get_test_db_conn():
    assert _db_conn is not None
    return _db_conn


def get_test_db():
    sess = Session(bind=_db_conn)

    try:
        yield sess
    finally:
        sess.close()


@pytest.fixture(scope="session", autouse=True)
def database():
    if database_exists(url):
        drop_database(url)
    create_database(url)
    Base.metadata.create_all(_db_conn)
    app.dependency_overrides[get_db] = get_test_db
    yield
    drop_database(url)


@pytest.yield_fixture
def session():
    db_session = Session(bind=_db_conn)

    yield db_session
    for tbl in reversed(Base.metadata.sorted_tables):
        _db_conn.execute(tbl.delete())
    db_session.close()


@pytest.fixture()
def client():
    with TestClient(app) as client:
        yield client


@pytest.fixture()
def data_user():
    return dict(
        name='tester',
        email='tester@email.com',
        age=18,
    )


@pytest.fixture()
def new_user(session, data_user):
    data = UserPost(
        name=data_user['name'],
        email=data_user['email'],
        age=data_user['age'],
    )
    return User.create(
        db_session=session,
        data=data
    )


@pytest.fixture()
def data_transaction():
    return dict(
        reference='reference',
        account='account',
        date='2020-02-02',
        amount=1.00,
        type='inflow',
        category='category',
    )


@pytest.fixture()
def new_transaction(session, new_user, data_transaction):
    data = TransactionPost(
        reference=data_transaction['reference'],
        account=data_transaction['account'],
        date=data_transaction['date'],
        amount=data_transaction['amount'],
        type=data_transaction['type'],
        category=data_transaction['category'],
    )
    return Transaction.create(
        db_session=session,
        user_id=new_user.id,
        data=data,
    )


@pytest.fixture()
def scenario(session, new_user):
    data_1 = dict(
        user_id=new_user.id,
        reference='000051',
        account='C00099',
        date='2020-01-03',
        amount=-51.13,
        type='outflow',
        category='groceries'
    )
    data_2 = dict(
        user_id=new_user.id,
        reference='000052',
        account='C00099',
        date='2020-01-10',
        amount=2500.72,
        type='inflow',
        category='salary'
    )
    data_3 = dict(
        user_id=new_user.id,
        reference='000053',
        account='C00099',
        date='2020-01-10',
        amount=-150.72,
        type='outflow',
        category='transfer'
    )
    data_4 = dict(
        user_id=new_user.id,
        reference='000054',
        account='C00099',
        date='2020-01-13',
        amount=-560.00,
        type='outflow',
        category='rent'
    )
    data_5 = dict(
        user_id=new_user.id,
        reference='000689',
        account='S00012',
        date='2020-01-10',
        amount=150.72,
        type='inflow',
        category='savings'
    )
    Transaction.create_bulk(
        db_session=session,
        data=[data_1, data_2, data_3, data_4, data_5]
    )
