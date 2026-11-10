# Factor Screener - Frontend

Vue 3 frontend for the Factor Screener (S&P 500 momentum scores).

## Tech stack

- Vue 3 (Composition API), Vue Router, Pinia
- Vite
- Lightweight Charts (charts)

## Structure

```
src/
├── assets/       # Global CSS and images
├── components/   # Reusable components
├── router/       # Route definitions
├── services/     # API calls (fetch)
│   └── serviceFetchApi.js   # HTTP client: base URL + error handling
├── stores/       # Pinia stores
├── views/        # One component per page
├── App.vue       # Root component
└── main.js       # Entry point
```

## Setup

Requires Node.js 22.18+ (or 24.12+).

```bash
cd frontend
npm install
cp .env.example .env     # optional: only needed to change the backend URL
npm run dev
```

The app runs on http://localhost:5173 and calls the backend on `VITE_API_URL`
(default `http://localhost:8000`). Start the backend first.

## Scripts

| Command           | Description                |
|-------------------|----------------------------|
| `npm run dev`     | Dev server with hot reload |
| `npm run build`   | Production build           |
| `npm run preview` | Preview the production build |

## Environment variables

| Variable       | Description          | Default                 |
|----------------|----------------------|-------------------------|
| `VITE_API_URL` | Backend API base URL | `http://localhost:8000` |
