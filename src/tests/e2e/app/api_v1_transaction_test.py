import pytest
from starlette.status import HTTP_200_OK
from starlette.status import HTTP_201_CREATED
from starlette.status import HTTP_400_BAD_REQUEST

from app import messages


def test_post_transactions_ok(client, new_user, data_transaction):
    data = dict(
        name=new_user.name,
        transactions=[data_transaction]
    )
    response = client.post(f"/api/v1/transactions/", json=data)
    assert response.status_code == HTTP_201_CREATED
    assert len(response.json()) == 1


def test_post_transactions_reference_already_exists(client, new_user, new_transaction, data_transaction):
    data = dict(
        name=new_user.name,
        transactions=[data_transaction]
    )
    response = client.post(f"/api/v1/transactions/", json=data)
    assert response.status_code == HTTP_201_CREATED
    assert len(response.json()) == 0


def test_post_transactions_reference_duplicated(client, new_user, data_transaction):
    data = dict(
        name=new_user.name,
        transactions=[data_transaction, data_transaction]
    )
    response = client.post(f"/api/v1/transactions/", json=data)
    assert response.status_code == HTTP_400_BAD_REQUEST
    assert response.json()['detail'] == messages.TRANSACTIONS_REFERENCES_ERROR


@pytest.mark.parametrize('type, amount',
                         [('inflow', -1.00),
                          ('outflow', 1.00)])
def test_post_transactions_amount_wrong(client, new_user, data_transaction, type, amount):
    data_transaction['type'] = type
    data_transaction['amount'] = amount
    data = dict(
        name=new_user.name,
        transactions=[data_transaction]
    )
    response = client.post(f"/api/v1/transactions/", json=data)
    assert response.status_code == HTTP_400_BAD_REQUEST
    assert response.json()['detail'] == messages.TRANSACTIONS_AMOUNTS_ERROR


def test_get_summary_by_account(client, new_user, scenario):
    response = client.get(f"/api/v1/transactions/{new_user.id}/summary_by_account")
    assert response.status_code == HTTP_200_OK
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
    assert response.json() == expected


def test_get_summary_by_category(client, new_user, scenario):
    response = client.get(f"/api/v1/transactions/{new_user.id}/summary_by_category")
    assert response.status_code == HTTP_200_OK
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
    assert response.json() == expected
