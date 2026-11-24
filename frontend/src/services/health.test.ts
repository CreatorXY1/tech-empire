import { afterEach, describe, expect, it, vi } from 'vitest'
import { getApiBaseUrl, getBackendHealth } from './health'

afterEach(() => {
  vi.unstubAllEnvs()
  vi.unstubAllGlobals()
})

describe('backend health client', () => {
  it('requires the API base URL to come from environment configuration', () => {
    vi.stubEnv('VITE_API_BASE_URL', '')

    expect(() => getApiBaseUrl()).toThrow('VITE_API_BASE_URL is required')
  })

  it('requests the versioned health endpoint using the configured base URL', async () => {
    vi.stubEnv('VITE_API_BASE_URL', 'http://localhost:8000/')
    const fetchMock = vi.fn().mockResolvedValue(
      new Response(JSON.stringify({ status: 'ok', service: 'tech-empire-api' }), {
        status: 200,
        headers: { 'Content-Type': 'application/json' },
      }),
    )
    vi.stubGlobal('fetch', fetchMock)

    await expect(getBackendHealth()).resolves.toEqual({
      status: 'ok',
      service: 'tech-empire-api',
    })
    expect(fetchMock).toHaveBeenCalledWith(
      'http://localhost:8000/api/v1/health',
      expect.objectContaining({ headers: { Accept: 'application/json' } }),
    )
  })
})
