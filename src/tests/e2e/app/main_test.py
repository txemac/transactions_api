from starlette.status import HTTP_200_OK


def test_check(client):
    response = client.get("/_check")
    assert response.status_code == HTTP_200_OK
    assert response.json() == dict(status='OK')
