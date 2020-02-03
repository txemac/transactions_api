def assert_dicts(body, expected):
    """
    Assert that check that the dict body contains all keys in expected.
    And the values are the same.
    If a value in expected contains "*" the value in body can be any value.

    :param body: dict with body of the response
    :param expected: dict with subset
    """
    for key in expected.keys():
        assert key in body.keys(), key
        if not expected[key] == '*':
            assert body[key] == expected[key], key
