import re
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
    def tokenize(self, sql_query):
        """
        Токенизирует SQL-запрос, разбивая его на лексемы (токены).
        """
        tokens = re.findall(r"\w+|[^\w\s]", sql_query.lower())
        return tokens
    
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
        Проверяет SQL-запросы на плагиат, сравнивая их сходство с использованием расстояния Левенштейна.
        """
        ref_code: str = data['ref_code']
        candidate_code: str = data['candidate_code']

        tokens1 = self.tokenize(ref_code)
        tokens2 = self.tokenize(candidate_code)
        
        matcher = SequenceMatcher(None, tokens1, tokens2)
        similarity_ratio = matcher.ratio()
        
        similarity_percentage = similarity_ratio * 100
        return CheckResult(percent=similarity_percentage)


class AntiplagService:
    """
    Основной сервис для проверки на плагиат.
    Обеспечивает интерфейс для проверки кода запросов.
    """
    def check(self, data: CheckInput):
        """
        Проверяет код запросов на наличие плагиата, используя SQLService.
        """ 
        service = SQLService()
        return service.check_plagiarism(data)


