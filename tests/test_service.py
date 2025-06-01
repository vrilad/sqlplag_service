import pytest
from src.service import AntiplagService, SQLService, CTEService
from src.entities import CheckInput
from unittest.mock import MagicMock

def test_antiplag_service_select_queries_ok(mocker):
    # Тестируем выбор SQLService для SELECT запросов
    test_data = CheckInput(
        ref_code="SELECT 1",
        candidate_code="SELECT 2"
    )
    
    mock_sql_service = mocker.MagicMock(spec=SQLService)
    mock_sql_service.check_plagiarism.return_value = {"percent": "90.0"}
    
    # Патчим создание SQLService
    mocker.patch('src.service.SQLService', return_value=mock_sql_service)
    
    service = AntiplagService()
    result = service.check(test_data)
    
    assert result == {"percent": "90.0"}
    mock_sql_service.check_plagiarism.assert_called_once_with(test_data)

def test_antiplag_service_cte_queries_ok(mocker):
    # Тестируем выбор CTEService для WITH запросов
    test_data = CheckInput(
        ref_code="WITH t AS (SELECT 1) SELECT * FROM t",
        candidate_code="WITH t AS (SELECT 2) SELECT * FROM t"
    )
    
    mock_cte_service = mocker.MagicMock(spec=CTEService)
    mock_cte_service.check_plagiarism.return_value = {"percent": "80.0"}
    
    # Патчим создание CTEService
    mocker.patch('src.service.CTEService', return_value=mock_cte_service)
    
    service = AntiplagService()
    result = service.check(test_data)
    
    assert result == {"percent": "80.0"}
    mock_cte_service.check_plagiarism.assert_called_once_with(test_data)

def test_sql_service_plagiarism_check_ok(mocker):
    # Тестируем SQLService (имитируем вызов cappa_sqlplag)
    test_data = CheckInput(
        ref_code="SELECT * FROM users",
        candidate_code="SELECT * FROM users WHERE id = 1"
    )
    
    mock_sql_plag = MagicMock()
    mock_sql_plag.similarity_percentage.return_value = "85.0"
    mocker.patch('cappa_sqlplag.SQLPlag', return_value=mock_sql_plag)
    
    service = SQLService()
    result = service.check_plagiarism(test_data)
    
    assert result == {"percent": "85.0"}
    mock_sql_plag.similarity_percentage.assert_called_once()

def test_cte_service_plagiarism_check_ok(mocker):
    # Тестируем CTEService (имитируем вызов cappa_sqlplag)
    test_data = CheckInput(
        ref_code="WITH t AS (SELECT 1) SELECT * FROM t",
        candidate_code="WITH t AS (SELECT 2) SELECT * FROM t"
    )
    
    mock_sql_plag = MagicMock()
    mock_sql_plag.cte_similarity_percentage.return_value = "75.0"
    mocker.patch('cappa_sqlplag.SQLPlag', return_value=mock_sql_plag)
    
    service = CTEService()
    result = service.check_plagiarism(test_data)
    
    assert result == {"percent": "75.0"}
    mock_sql_plag.cte_similarity_percentage.assert_called_once()