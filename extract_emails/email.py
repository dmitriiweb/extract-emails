from typing import Dict, List


class Email:
    """Email representation

    :param str email: email
    :param str source_page: source page
    """

    def __init__(self, email: str, source_page: str):
        self.email = email
        self.source_page = source_page

    def __repr__(self):
        return f'Email(email="{self.email}", source_page="{self.source_page}")'

    def as_dict(self) -> Dict[str, str]:
        """Convert Email to Dict

        :return: Email as dict
        """
        return {"email": self.email, "source_page": self.source_page}

    def as_list(self) -> List[str]:
        """Convert Email to List

        :return: Email as list
        """
        return [self.email, self.source_page]
