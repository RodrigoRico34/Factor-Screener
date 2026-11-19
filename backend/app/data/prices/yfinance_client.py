from app.data.prices.prices_fetcher import PriceSource, PriceFetchError
from datetime import datetime, timedelta
import pandas as pd
import yfinance as yf


class YFinanceClient(PriceSource):
    def get_prices(self, tickers: list[str]):
        """
        Fetch adjusted close prices for the given tickers via Yahoo Finance.

        Args:
            tickers: List of ticker symbols, e.g. ["AAPL", "MSFT"]

        Returns:
            list[dict]: List of dicts with keys ticker, date, close,
                        e.g. [{"ticker": "AAPL", "date": datetime.date(2024, 1, 15), "close": 185.92}, ...]

        Raises:
            PriceFetchError: If the data cannot be retrieved or parsed.

        Example:
            YFinanceClient().get_prices(["AAPL", "MSFT"])
        """
        # Fix Yahoo Finance ticker format (BRK.B -> BRK-B)
        yf_tickers = [t.replace('.', '-') for t in tickers]

        end = datetime.now().strftime("%Y-%m-%d")
        start = (datetime.now() - timedelta(days=5 * 365)).strftime("%Y-%m-%d")

        try:
            data = yf.download(yf_tickers, start=start, end=end, auto_adjust=True, threads=False)
        except Exception as exc:
            raise PriceFetchError(f"yfinance download failed: {exc}")

        if data.empty:
            raise PriceFetchError("yfinance returned no data")

        # yfinance 1.x returns MultiIndex columns (Price, Ticker).
        if isinstance(data.columns, pd.MultiIndex):
            prices = data["Close"]
        else:
            prices = data[["Close"]]
            prices.columns = yf_tickers

        # If only one ticker, prices is a Series (not a DataFrame).
        # Convert to DataFrame so the loop below works in both cases.
        if isinstance(prices, pd.Series):
            prices = prices.to_frame(name=yf_tickers[0])

        results = []
        for yf_ticker in prices.columns:
            # Reverse the fix to get back the original ticker (BRK-B -> BRK.B)
            original_ticker = yf_ticker.replace('-', '.')
            series = prices[yf_ticker].dropna()

            for date, close in series.items():
                results.append({
                    "ticker": original_ticker,
                    "date": date.date(),
                    "close": round(float(close), 4),
                })

        return results