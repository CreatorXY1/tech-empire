export type ConnectionState = 'checking' | 'connected' | 'disconnected'

type HealthResponse = {
  status: 'ok'
  service: string
}

function getApiBaseUrl(): string {
  const apiBaseUrl = import.meta.env.VITE_API_BASE_URL?.trim().replace(/\/$/, '')
  if (!apiBaseUrl) {
    throw new Error('VITE_API_BASE_URL is required to connect to the backend')
  }
  return apiBaseUrl
}

export async function getBackendHealth(signal?: AbortSignal): Promise<HealthResponse> {
  const response = await fetch(`${getApiBaseUrl()}/api/v1/health`, {
    headers: { Accept: 'application/json' },
    signal,
  })

  if (!response.ok) {
    throw new Error(`Backend health check failed with status ${response.status}`)
  }

  const result: unknown = await response.json()
  if (!isHealthResponse(result)) {
    throw new Error('Backend returned an unexpected health response')
  }

  return result
}

export { getApiBaseUrl }

function isHealthResponse(value: unknown): value is HealthResponse {
  return typeof value === 'object' && value !== null && 'status' in value && value.status === 'ok' && 'service' in value && typeof value.service === 'string'
}
