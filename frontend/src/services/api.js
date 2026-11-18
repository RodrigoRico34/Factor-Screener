/**
 * Author:      Samuel Theytaz
 * Created:     17.11.2026
 * Modified:    18.11.2026
 * Description: Functions to call the backend from any component (stocks, sectors and backtest)
 *              The HTTP errors are sent back as an ApiError with the status code
 *              Counts the requests in progress to show the loading spinner
 */

import { ref } from 'vue'

const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

// Number of requests waiting for an answer, the spinner is shown while it's above 0
export const pendingRequests = ref(0)

// status is 0 when the backend can't be reached
export class ApiError extends Error {
  constructor(message, status) {
    super(message)
    this.name = 'ApiError'
    this.status = status
  }
}

async function request(path, options = {}) {
  pendingRequests.value++

  try {
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

    return await response.json()
  } finally {
    // also runs when there is an error, so the spinner never stays on screen
    pendingRequests.value--
  }
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
