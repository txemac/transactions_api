import pytest

from app.utils import check_amounts
from app.utils import check_references
from database.schemas import TransactionPost
from database.schemas import TransactionPostList


@pytest.mark.parametrize('transactions, expected',
                         [(TransactionPostList(
                             transactions=[
                                 TransactionPost(reference='a01', account='aaa', date='2020-01-01', amount=1.00,
                                                 type='inflow', category='food'),
                                 TransactionPost(reference='a01', account='aaa', date='2020-01-01', amount=1.00,
                                                 type='inflow', category='food')]), False),
                             (TransactionPostList(
                                 transactions=[
                                     TransactionPost(reference='a01', account='aaa', date='2020-01-01', amount=1.00,
                                                     type='inflow', category='food'),
                                     TransactionPost(reference='a02', account='aaa', date='2020-01-01', amount=1.00,
                                                     type='inflow', category='food')]), True)
                         ])
def test_check_references(transactions, expected):
    assert check_references(transactions=transactions) is expected


@pytest.mark.parametrize('transactions, expected',
                         [(TransactionPostList(
                             transactions=[
                                 TransactionPost(reference='a01', account='aaa', date='2020-01-01', amount=1.00,
                                                 type='inflow', category='food')]), True),
                             (TransactionPostList(
                                 transactions=[
                                     TransactionPost(reference='a01', account='aaa', date='2020-01-01', amount=-1.00,
                                                     type='inflow', category='food')]), False),
                             (TransactionPostList(
                                 transactions=[
                                     TransactionPost(reference='a02', account='aaa', date='2020-01-01', amount=0.00,
                                                     type='inflow', category='food')]), True),
                             (TransactionPostList(
                                 transactions=[
                                     TransactionPost(reference='a02', account='aaa', date='2020-01-01', amount=-0.00,
                                                     type='inflow', category='food')]), True),
                             (TransactionPostList(
                                 transactions=[
                                     TransactionPost(reference='a02', account='aaa', date='2020-01-01', amount=1.00,
                                                     type='outflow', category='food')]), False),
                             (TransactionPostList(
                                 transactions=[
                                     TransactionPost(reference='a02', account='aaa', date='2020-01-01', amount=-1.00,
                                                     type='outflow', category='food')]), True),
                             (TransactionPostList(
                                 transactions=[
                                     TransactionPost(reference='a02', account='aaa', date='2020-01-01', amount=0.00,
                                                     type='outflow', category='food')]), True),
                             (TransactionPostList(
                                 transactions=[
                                     TransactionPost(reference='a02', account='aaa', date='2020-01-01', amount=-0.00,
                                                     type='outflow', category='food')]), True)
                         ])
def test_check_amount(transactions, expected):
    assert check_amounts(transactions=transactions) is expected