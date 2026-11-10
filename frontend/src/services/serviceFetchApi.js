// Server address only: the routes (/companies, /price/AAPL, ...) are added by each service.
const API_BASE_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'

function httpError(status) {
  const error = new Error(`Request failed with status ${status}`)
  error.status = status
  return error
}

// Small HTTP client: returns the parsed JSON, or throws if the server answers with a non-2xx status.
// `options` is passed to fetch as is (e.g. { signal } to cancel a request).
export async function request(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, options)
  if (!response.ok) throw httpError(response.status)
  return response.json()
}
