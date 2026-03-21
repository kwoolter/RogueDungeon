
class BaseException(Exception):
    def __init__(self, name : str, description : str):
        super().__init__()
        self.name = name
        self.description = description

    def __str__(self):
        text = f"{self.name}: {self.description}"
        return text

class ApplicationException(BaseException):
    def __init__(self, name, description):
        super().__init__(name, description)


class ErrorException(BaseException):
    def __init__(self, name, description):
        super().__init__(name, description)