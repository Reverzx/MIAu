def assert_json_response(expected, actual):
    for key, value in expected.items():
        assert key in actual, f'Missing key: {key}'
        if isinstance(value, dict):
            assert isinstance(actual[key], dict), \
                f"Expected dict at {key}, got {type(actual[key])}"
            assert_json_response(value, actual[key])
        else:
            assert actual[key] == value, f"Mismatch at {key}: expected {value}, got {actual[key]}"
