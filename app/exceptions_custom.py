import re


class IntegrityDataException(Exception):
    def __init__(self, message: str) -> None:
        detail_text = re.search(r"DETAIL: (.+)", message)
        if detail_text:
            message = detail_text.group(1).strip()
            super().__init__(message)


class UserNotFoundException(Exception):
    pass
