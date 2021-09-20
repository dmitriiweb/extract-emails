from abc import ABC, abstractmethod
from typing import List


class EmailFilterInterface(ABC):
    """
    Interface for email filters
    """

    @abstractmethod
    def filter(self, emails: List[str]) -> List[str]:
        """
        Filter emails by params

        :param: list(str) emails: list of emails for filtering
        :return: Filtered list of emails
        """
        pass
