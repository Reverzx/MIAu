from jsonschema import validate
# from loguru import logger

def validate_response_schema(expected_schema, actual_schema):
    try:
        validate(actual_schema, expected_schema)
        print("JSON-response matches the schema")
    except Exception as e:
        print("JSON-response does not match the schema:", e)


#  def is_response_schema_correct(self, response, expected_schema):
        # """
        # Checks if response JSON fits to expected schema.
        # Returns True if response fits, otherwise False
        # """
        # current_schema = response.json()
        # try:
        #     validate(current_schema, expected_schema)
        #     return True
        # except ValidationError as v:
        #     logger.warning(f"JSON schema validation error: {v}")
        #     return False
