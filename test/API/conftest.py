from pathlib import Path
import json
import pytest


@pytest.fixture
def read_schema():
    path = Path(__file__).parents[2] / "test_data" / "response_schemas.json"
    with path.open() as f:
        return json.load(f)
