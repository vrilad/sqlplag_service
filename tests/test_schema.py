import pytest
from src.schema import CheckSchema, BadRequestSchema
from marshmallow import ValidationError

def test_check_schema_valid_data_ok():
    # Тестируем валидацию корректных данных
    valid_data = {
        "ref_code": "SELECT 1",
        "candidate_code": "SELECT 2"
    }
    
    schema = CheckSchema()
    result = schema.load(valid_data)
    
    assert result["ref_code"] == "SELECT 1"
    assert result["candidate_code"] == "SELECT 2"

def test_check_schema_missing_fields_raise_exception():
    # Тестируем валидацию с отсутствующими обязательными полями
    invalid_data = {
        "ref_code": "SELECT 1"
        # Пропущено candidate_code
    }
    
    schema = CheckSchema()
    with pytest.raises(ValidationError) as excinfo:
        schema.load(invalid_data)
    
    assert "candidate_code" in str(excinfo.value)

def test_bad_request_schema_error_details():
    # Тестируем сериализацию ошибки валидации
    description = type('Description', (), {'messages': {"field": ["Error message"]}})
    error = type('Error', (), {'description': description})()
    
    schema = BadRequestSchema()
    result = schema.dump(error)
    
    assert result["error"] == "ValidationError"
    assert result["details"] == {"field": ["Error message"]}