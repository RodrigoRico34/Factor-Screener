from app.data.database import SessionLocal
from app.core.stocks import import_stocks_core
from app.core.prices import import_prices_core
from app.core.factors import compute_momentum_core, classify_deciles_core
from app.data.tickers.sp500_github_client import SP500Github
from app.data.prices.yfinance_client import YFinanceClient


def seed():
    db = SessionLocal()

    try:
        print("1/4 - Importing tickers...")
        tickers_result = import_stocks_core(db, SP500Github)
        print(f"      {tickers_result['imported']} tickers imported")

        print("2/4 - Importing prices...")
        prices_result = import_prices_core(db, YFinanceClient)
        print(f"      {prices_result['imported']} prices imported")

        print("3/4 - Computing momentum...")
        momentum_result = compute_momentum_core(db)
        print(f"      {momentum_result['computed']} scores computed")

        print("4/4 - Classifying deciles...")
        deciles_result = classify_deciles_core(db)
        print(f"      {deciles_result['classified']} stocks classified")

        print("\n--- Summary ---")
        print(f"Tickers:  {tickers_result['imported']}")
        print(f"Prices:   {prices_result['imported']}")
        print(f"Scores:   {momentum_result['computed']}")
        print(f"Deciles:  {deciles_result['classified']}")

    finally:
        db.close()


if __name__ == "__main__":
    seed()