import { act, render, screen, waitFor } from '@testing-library/react'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import App from './App'
import { getBackendHealth } from '../services/health'

vi.mock('../services/health', () => ({
  getBackendHealth: vi.fn(),
}))

const mockHealthCheck = vi.mocked(getBackendHealth)

describe('Tech Empire application shell', () => {
  beforeEach(() => {
    mockHealthCheck.mockReset()
  })

  it('shows checking while the health request is pending', () => {
    mockHealthCheck.mockReturnValue(new Promise(() => undefined))

    render(<App />)

    expect(screen.getByRole('status').textContent).toContain('Checking connection')
  })

  it('shows connected when the backend responds successfully', async () => {
    mockHealthCheck.mockResolvedValue({ status: 'ok', service: 'tech-empire-api' })

    render(<App />)

    await waitFor(() => expect(screen.getByRole('status').textContent).toContain('Connected'))
  })

  it('shows disconnected when the health request fails', async () => {
    mockHealthCheck.mockRejectedValue(new Error('Backend is unavailable'))

    render(<App />)

    await waitFor(() => expect(screen.getByRole('status').textContent).toContain('Disconnected'))
  })

  it('times out stalled requests and periodically retries', async () => {
    vi.useFakeTimers()
    mockHealthCheck.mockImplementation((signal) => new Promise((_, reject) => {
      signal?.addEventListener('abort', () => reject(new DOMException('Aborted', 'AbortError')))
    }))

    render(<App />)
    expect(screen.getByRole('status').textContent).toContain('Checking connection')

    await act(async () => {
      await vi.advanceTimersByTimeAsync(5_000)
    })
    expect(screen.getByRole('status').textContent).toContain('Disconnected')

    await act(async () => {
      await vi.advanceTimersByTimeAsync(25_000)
    })
    expect(mockHealthCheck).toHaveBeenCalledTimes(2)
    vi.useRealTimers()
  })
})
