from jsonschema import validate, ValidationError
from loguru import logger


def validate_response_schema(expected_schema, actual_schema):
    """
    Checks if response JSON fits to expected schema.
    Returns True if response fits, otherwise False
    """
    try:
        validate(expected_schema, actual_schema)
        logger.success("JSON-response matches the schema")
        return True
    except ValidationError as v:
        logger.warning(f"JSON schema validation error: {v}")
        return False
