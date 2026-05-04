const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? ''

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...(options.headers || {})
    },
    ...options,
    body: options.body ? JSON.stringify(options.body) : undefined
  })

  const responseText = await response.text()
  const payload = responseText ? JSON.parse(responseText) : null

  if (!response.ok) {
    const error = new Error(
      payload?.error ||
        payload?.reasons?.join(', ') ||
        payload?.details ||
        'Request failed'
    )

    error.status = response.status
    error.details = payload
    throw error
  }

  return payload
}

export function get(path) {
  return request(path, { method: 'GET' })
}

export function post(path, body) {
  return request(path, { method: 'POST', body })
}