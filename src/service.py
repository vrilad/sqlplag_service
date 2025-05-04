import re
import cappa_sqlplag
from difflib import SequenceMatcher
from abc import ABC, abstractmethod
from .entities import (
    CheckInput,
    CheckResult
)

class AntiplagBaseService(ABC):
    """
    Базовый абстрактный класс для сервисов проверки на плагиат.
    """    
    @abstractmethod
    def check_plagiarism(self, data: CheckInput):
        """
        Абстрактный метод для проверки на плагиат.
        """
        pass

class SQLService(AntiplagBaseService):
    """
    Сервис для проверки SQL-запросов на плагиат.
    """
    def check_plagiarism(self, data: CheckInput):
        """
        Проверяет SQL-запросы, начинающиеся с Select, на плагиат.
        """
        ref_code: str = data['ref_code']
        candidate_code: str = data['candidate_code']

        sqlplag = cappa_sqlplag.SQLPlag(ref_code=ref_code, candidate_code=candidate_code) 
        similarity_percentage = sqlplag.similarity_percentage()
        
        return CheckResult(percent=similarity_percentage)
    
class CTEService(AntiplagBaseService):
        
    def check_plagiarism(self, data: CheckInput):
        """
        Проверяет SQL-запросы, начинающиеся с With, на плагиат.
        """
        ref_code: str = data['ref_code']
        candidate_code: str = data['candidate_code']

        sqlplag = cappa_sqlplag.SQLPlag(ref_code=ref_code, candidate_code=candidate_code) 
        similarity_percentage = sqlplag.cte_similarity_percentage()
        
        return CheckResult(percent=similarity_percentage)


class AntiplagService:
    """
    Основной сервис для проверки на плагиат.
    Обеспечивает интерфейс для проверки кода запросов.
    """
    def check(self, data: CheckInput):
        """
        Проверяет код запросов на наличие плагиата, используя сервисы.
        """ 
        ref_code: str = data['ref_code']
        candidate_code: str = data['candidate_code']

        if all(code.lower().startswith('select') for code in (ref_code, candidate_code)):
            service = SQLService()
        else:
            service = CTEService()

        return service.check_plagiarism(data)


