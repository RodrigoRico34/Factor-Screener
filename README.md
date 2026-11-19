# Factor Screener

A momentum factor screener for S&P 500 stocks. The app ranks every stock by its 12-month cumulative return, assigns deciles (1 = losers, 10 = winners), and displays the results in a sortable, filterable table.

## Tech Stack

**Backend**

- Python 3.12
- FastAPI
- SQLAlchemy (ORM)
- MySQL (via PyMySQL)
- pandas / numpy (momentum computation)
- yfinance (price data)

**Frontend**

- Vue.js 3 (Composition API, `<script setup>`)
- Vue Router
- Vite
- Lightweight Charts (TradingView)

## Project Structure

```
backend/
  app/
    api/router/      # FastAPI route handlers
    core/            # Business logic (momentum, deciles)
    data/
      models/        # SQLAlchemy models + query helpers
      tickers/       # S&P 500 ticker fetchers
      prices/        # Price data clients (yfinance)
    schemas/         # Pydantic response schemas
  seed.py            # Database seed script
frontend/
  src/
    views/           # Page components (Ranking, Detail, Backtest)
    components/      # Shared components (NavBar)
    services/        # API client
    router/          # Vue Router config
    assets/          # Global CSS, logo
```

## Prerequisites

- Python 3.12+
- Node.js 22+
- MySQL 8+ (running, with an empty database created)

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/RodrigoRico34/Factor-Screener.git
cd Factor-Screener
```

### 2. Backend setup

```bash
cd backend
python -m venv .venv
```

Activate the virtual environment:

```bash
# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file at the project root (next to `requirements.txt`):

```
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/factor_screener
```

Replace `user`, `password`, and `factor_screener` with your MySQL credentials and database name.

### 3. Frontend setup

```bash
cd frontend
npm install
```

Create a `.env.local` file inside `frontend/`:

```
VITE_API_URL=http://localhost:8000
```

## Usage

### Seed the database

The seed script imports S&P 500 tickers, fetches historical prices, computes momentum scores, and classifies deciles. Run it once before starting the app:

```bash
cd backend
python -m seed
```

This takes a few minutes (fetching ~500 tickers from yfinance).

### Start the backend

```bash
cd backend
uvicorn app.main:app --reload
```

The API runs at `http://localhost:8000`. Check `http://localhost:8000/docs` for the interactive Swagger UI.

### Start the frontend

```bash
cd frontend
npm run dev