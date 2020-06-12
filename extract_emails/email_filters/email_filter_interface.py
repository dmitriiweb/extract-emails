from abc import ABC, abstractmethod
from typing import List


class EmailFilterInterface(ABC):
    """
    Interface for email filters

    :param str emails_list: List of emails, example: [example.com, ]
    """
    def __init__(self, emails_list: List[str]):
        self.emails = emails_list

    @abstractmethod
    def filter(self) -> List[str]:
        """
        Filter emails by params

        :return: Filtered list of emails
        """
        pass
