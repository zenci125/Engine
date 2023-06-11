class EngException(Exception):
    pass


class EngineException(EngException):
    NOT_FOUND = "This property not found"
    NOT_PERMISSION = "Have not root to delete all properties"
    NOT_FOUND_FILE = "File does not exist"