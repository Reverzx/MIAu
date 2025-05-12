from jsonschema import validate


def validate_response_schema(expected_schema, actual_schema):
    try:
        validate(actual_schema, expected_schema)
        print("JSON-response matches the schema")
    except Exception as e:
        print("JSON-response does not match the schema:", e)
