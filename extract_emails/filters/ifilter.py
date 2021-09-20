from abc import ABC
from abc import abstractmethod
from typing import Iterable
from typing import List


class IFilter(ABC):
    """Interface for filters"""

    @abstractmethod
    def filter(self, values: Iterable[str]) -> List[str]:
        """Filter values

        Args:
            values: unfiltered values

        Returns:
            Filtered values
        """
        pass
