import pytest
from pydantic import ValidationError

from database.schemas import TransactionPost
from database.schemas import UserPost


def test_user_post_ok():
    assert UserPost(name='name', email='email', age=18) is not None


@pytest.mark.parametrize('name', ['a', None, 12, 'a' * 151])
def test_user_post_name_wrong(name):
    with pytest.raises(ValidationError):
        UserPost(name=name, email='email', age=18)


@pytest.mark.parametrize('email', ['a', None, 12, 'a' * 151])
def test_user_post_email_wrong(email):
    with pytest.raises(ValidationError):
        UserPost(name='name', email=email, age=18)


@pytest.mark.parametrize('age', ['a', None, -1])
def test_user_post_age_wrong(age):
    with pytest.raises(ValidationError):
        UserPost(name='name', email='email', age=age)


def test_transaction_post_ok():
    assert TransactionPost(
        reference='reference',
        account='account',
        date='2020-02-02',
        type='inflow',
        amount=1.00,
        category='category',
    ) is not None


@pytest.mark.parametrize('reference', ['a', None, 12, 'a' * 151])
def test_transaction_post_reference_wrong(reference):
    with pytest.raises(ValidationError):
        TransactionPost(
            reference=reference,
            account='account',
            date='2020-02-02',
            type='inflow',
            amount=1.00,
            category='category',
        )


@pytest.mark.parametrize('account', ['a', None, 12, 'a' * 151])
def test_transaction_post_account_wrong(account):
    with pytest.raises(ValidationError):
        TransactionPost(
            reference='reference',
            account=account,
            date='2020-02-02',
            type='inflow',
            amount=1.00,
            category='category',
        )


@pytest.mark.parametrize('date', ['a', None, '2020-02-31'])
def test_transaction_post_date_wrong(date):
    with pytest.raises(ValidationError):
        TransactionPost(
            reference='reference',
            account='account',
            date=date,
            type='inflow',
            amount=1.00,
            category='category',
        )


@pytest.mark.parametrize('amount', ['a', None])
def test_transaction_post_amount_wrong(amount):
    with pytest.raises(ValidationError):
        TransactionPost(
            reference='reference',
            account='account',
            date='2020-02-02',
            type='inflow',
            amount=amount,
            category='category',
        )


@pytest.mark.parametrize('type', ['a', None, 'error', 1])
def test_transaction_post_type_wrong(type):
    with pytest.raises(ValidationError):
        TransactionPost(
            reference='reference',
            account='account',
            date='2020-02-02',
            type=type,
            amount=1.00,
            category='category',
        )


@pytest.mark.parametrize('category', ['a', None, -1])
def test_transaction_post_category_wrong(category):
    with pytest.raises(ValidationError):
        TransactionPost(
            reference='reference',
            account='account',
            date='2020-02-02',
            type='inflow',
            amount=1.00,
            category=category,
        )
