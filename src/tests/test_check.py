from starlette.status import HTTP_200_OK


def test_check(test_app):
    response = test_app.get("/_check")
    assert response.status_code == HTTP_200_OK
    assert response.json() == dict(message='OK')
