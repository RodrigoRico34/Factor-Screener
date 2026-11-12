from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.router.stocks import router as stocks_router

app = FastAPI(
    title="Factor Screener",
    description="S&P 500 Momentum Factor Screener API",
    version="1.0.0",
)

# Allow the Vue.js frontend to communicate with the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with the frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(stocks_router)

@app.get("/")
def health_check():
    """Health check endpoint to verify the server is running."""
    return {"status": "ok", "message": "Factor Screener API is running"}

