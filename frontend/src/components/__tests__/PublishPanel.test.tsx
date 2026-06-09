import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { PublishPanel } from '../PublishPanel'

const mockFetch = vi.fn()
vi.stubGlobal('fetch', mockFetch)

afterEach(() => {
  vi.clearAllMocks()
})

describe('PublishPanel — 一鍵發布 + 備份確認', () => {
  it('renders publish button', () => {
    render(<PublishPanel content="test" platforms={['threads']} />)
    expect(screen.getByRole('button', { name: /發布/ })).toBeInTheDocument()
  })

  it('disables button when no content', () => {
    render(<PublishPanel content="" platforms={['threads']} />)
    expect(screen.getByRole('button', { name: /發布/ })).toBeDisabled()
  })

  it('disables button when no platform selected', () => {
    render(<PublishPanel content="hello" platforms={[]} />)
    expect(screen.getByRole('button', { name: /發布/ })).toBeDisabled()
  })

  it('shows loading state while publishing', async () => {
    mockFetch.mockResolvedValue({
      ok: true,
      json: async () => ({ sha256: 'abc123', proof_timestamp: '2026-01-01T00:00:00Z' }),
    })
    const user = userEvent.setup()
    render(<PublishPanel content="攝影日記" platforms={['threads']} />)
    await user.click(screen.getByRole('button', { name: /發布/ }))
    expect(screen.getByText(/發布中/)).toBeInTheDocument()
  })

  it('shows backup confirmation with sha256 after success', async () => {
    mockFetch.mockResolvedValue({
      ok: true,
      json: async () => ({ sha256: 'deadbeef1234', proof_timestamp: '2026-06-09T12:00:00Z' }),
    })
    const user = userEvent.setup()
    render(<PublishPanel content="攝影日記" platforms={['threads']} />)
    await user.click(screen.getByRole('button', { name: /發布/ }))
    await waitFor(() =>
      expect(screen.getByText(/deadbeef1234/)).toBeInTheDocument()
    )
    expect(screen.getByText(/備份完成/)).toBeInTheDocument()
  })

  it('shows error message on publish failure', async () => {
    mockFetch.mockResolvedValue({ ok: false, json: async () => ({}) })
    const user = userEvent.setup()
    render(<PublishPanel content="失敗測試" platforms={['threads']} />)
    await user.click(screen.getByRole('button', { name: /發布/ }))
    await waitFor(() =>
      expect(screen.getByText(/發布失敗/)).toBeInTheDocument()
    )
  })
})
