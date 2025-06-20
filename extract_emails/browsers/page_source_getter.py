from __future__ import annotations

from abc import ABC, abstractmethod


class PageSourceGetter(ABC):
    """All browsers must inherit from this class"""

    def __enter__(self) -> PageSourceGetter:
        """Context manager enter method.

        Returns:
            Self instance for method chaining
        """
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit method.

        Args:
            exc_type: Exception type
            exc_val: Exception value
            exc_tb: Exception traceback
        """
        self.stop()

    async def __aenter__(self) -> PageSourceGetter:
        """Async context manager enter method.

        Returns:
            Self instance for method chaining
        """
        await self.astart()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Async context manager exit method.

        Args:
            exc_type: Exception type
            exc_val: Exception value
            exc_tb: Exception traceback
        """
        await self.astop()

    @abstractmethod
    def start(self) -> None: ...

    @abstractmethod
    def stop(self) -> None: ...

    @abstractmethod
    async def astart(self) -> None: ...

    @abstractmethod
    async def astop(self) -> None: ...

    @abstractmethod
    def get_page_source(self, url: str) -> str:
        """Return page content from an URL

        Args:
            url: URL

        Returns:
            page content (html, json, whatever)
        """
        ...

    @abstractmethod
    async def aget_page_source(self, url: str) -> str:
        """Return page content from an URL asynchronously

        Args:
            url: URL

        Returns:
            page content (html, json, whatever)
        """
        ...
