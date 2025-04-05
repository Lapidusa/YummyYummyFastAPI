from typing import Any, Optional

class ResponseUtils:
    @staticmethod
    def success(**kwargs) -> dict:
        response = {"result": True}
        response.update(kwargs)
        return response

    @staticmethod
    def error(message: str = "Произошла ошибка") -> dict:
        return {"result": False, "message": message}