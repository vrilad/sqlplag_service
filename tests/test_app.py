import pytest
from main import create_app
from src.entities import CheckResult
from src.service import AntiplagService, SQLService, CTEService
from marshmallow import ValidationError

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_check_endpoint_with_select_queries_ok(client, mocker):
    # Мокируем AntiplagService чтобы не зависеть от реальной реализации
    mock_result = CheckResult(percent="85.0")
    mocker.patch.object(AntiplagService, 'check', return_value=mock_result)
    
    # Тестовые данные - SELECT запросы
    test_data = {
        "ref_code": "SELECT * FROM users",
        "candidate_code": "SELECT * FROM users WHERE id = 1"
    }
    
    response = client.post('/check/', json=test_data)
    
    assert response.status_code == 200
    assert response.json == {"percent": "85.0"}

def test_check_endpoint_with_cte_queries_ok(client, mocker):
    mock_result = CheckResult(percent="75.0")
    mocker.patch.object(AntiplagService, 'check', return_value=mock_result)
    
    # Тестовые данные - WITH запросы
    test_data = {
        "ref_code": "WITH temp AS (SELECT * FROM users) SELECT * FROM temp",
        "candidate_code": "WITH temp AS (SELECT id FROM users) SELECT * FROM temp"
    }
    
    response = client.post('/check/', json=test_data)
    
    assert response.status_code == 200
    assert response.json == {"percent": "75.0"}

def test_check_endpoint_with_missing_fields_raise_exception(client):
    # Отправляем запрос без обязательных полей
    test_data = {"ref_code": "SELECT 1"}
    
    response = client.post('/check/', json=test_data)
    
    assert response.status_code == 400
    assert "ValidationError" in response.json["error"]
    assert "candidate_code" in response.json["details"]