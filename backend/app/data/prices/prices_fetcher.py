from abc import ABC, abstractmethod


class PriceSource(ABC):
    @abstractmethod
    def get_prices(self, tickers: list[str]):
        """
        Fetch adjusted close prices for the given tickers.

        Args:
            tickers: List of ticker symbols, e.g. ["AAPL", "MSFT", ...]

        Returns:
            list[dict]: List of dicts with keys ticker, date, close,
                        e.g. [{"ticker": "AAPL", "date": "2024-01-15", "close": 185.92}, ...]

        Raises:
            PriceFetchError: If the data cannot be retrieved or parsed.
        """
        pass


class PriceFetchError(Exception):
    pass