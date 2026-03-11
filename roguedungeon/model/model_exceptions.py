
class BaseException(Exception):
    def __init__(self, name : str, description : str):
        super().__init__()
        self.name = name
        self.description = description

    def __str__(self):
        text = f"{self.name} - {self.description}"
        return text

class ApplicationException(Exception):
    def __init__(self, name, description):
        super().__init__(name, description)

    def __str__(self):
        text = super().__str__()
        return text