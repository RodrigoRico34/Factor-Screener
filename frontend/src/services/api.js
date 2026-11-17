/**
 * Author:      Samuel Theytaz
 * Created:     17.11.2026
 * Modified:    17.11.2026
 * Description: Functions to call the backend from any component (stocks, sectors and backtest)
 *              The HTTP errors are sent back as an ApiError with the status code
 */

const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

// status is 0 when the backend can't be reached
export class ApiError extends Error {
  constructor(message, status) {
    super(message)
    this.name = 'ApiError'
    this.status = status
  }
}

async function request(path, options = {}) {
  let response

  try {
    response = await fetch(BASE_URL + path, options)
  } catch {
    throw new ApiError('Backend unreachable', 0)
  }

  if (!response.ok) {
    // FastAPI puts the error message in "detail"
    const body = await response.json().catch(() => ({}))
    const message = typeof body.detail === 'string' ? body.detail : `HTTP error ${response.status}`
    throw new ApiError(message, response.status)
  }

  return response.json()
}

export function getStocks() {
  return request('/stocks')
}

export function getStock(ticker) {
  return request(`/stocks/${encodeURIComponent(ticker)}`)
}

export function getSectors() {
  return request('/sectors')
}

export function runBacktest() {
  return request('/backtest', { method: 'POST' })
}
