import pytest
from starlette.status import HTTP_200_OK
from starlette.status import HTTP_201_CREATED
from starlette.status import HTTP_404_NOT_FOUND
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from app import messages


def test_post_transactions_ok(client, new_user, data_transaction):
    data = dict(
        name=new_user.name,
        transactions=[data_transaction]
    )
    response = client.post(f"/api/v1/transactions/", json=data)
    assert response.status_code == HTTP_201_CREATED


def test_post_transactions_reference_already_exists(client, new_user, new_transaction, data_transaction):
    data = dict(
        name=new_user.name,
        transactions=[data_transaction]
    )
    response = client.post(f"/api/v1/transactions/", json=data)
    assert response.status_code == HTTP_201_CREATED


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
    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json()['detail'][0]['msg'] == messages.TRANSACTIONS_AMOUNTS_ERROR


def test_get_summary_by_account_ok(client, new_user, scenario):
    response = client.get(f"/api/v1/transactions/summary_by_account?name={new_user.name}")
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


def test_get_summary_by_account_user_not_found(client, new_user, scenario):
    response = client.get("/api/v1/transactions/summary_by_account?name=hola")
    assert response.status_code == HTTP_404_NOT_FOUND
    assert response.json()['detail'] == messages.USER_NOT_FOUND


def test_get_summary_by_category_ok(client, new_user, scenario):
    response = client.get(f"/api/v1/transactions/summary_by_category?name={new_user.name}")
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


def test_get_summary_by_category_user_not_found(client, new_user, scenario):
    response = client.get("/api/v1/transactions/summary_by_category?name=hola")
    assert response.status_code == HTTP_404_NOT_FOUND
    assert response.json()['detail'] == messages.USER_NOT_FOUND
