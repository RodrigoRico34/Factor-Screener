from abc import ABC, abstractmethod

class TickerSource(ABC):
    @abstractmethod
    def get_tickers(self):
        """
        Fetch the list of tickers with name and GICS sector for the target universe.

        Returns:
            list[dict]: List of dicts with keys Symbol, Name, Sector,
                        e.g. [{"Symbol": "AAPL", "Name": "Apple Inc.", "Sector": "Information Technology"}, ...]

        Raises:
            TickerFetchError: If the data cannot be retrieved or parsed.
        """
        pass

class TickerFetchError(Exception):
    pass