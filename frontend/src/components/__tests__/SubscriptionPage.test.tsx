import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { SubscriptionPage } from '../SubscriptionPage'

const mockFetch = vi.fn()
vi.stubGlobal('fetch', mockFetch)

afterEach(() => {
  vi.clearAllMocks()
})

const ACTIVE_SUB = {
  plan: 'pro',
  status: 'active',
  trial_ends_at: null,
  current_period_end: '2026-07-09T00:00:00Z',
}

const TRIALING_SUB = {
  plan: 'free',
  status: 'trialing',
  trial_ends_at: '2026-06-23T00:00:00Z',
  current_period_end: null,
}

describe('SubscriptionPage — 訂閱管理', () => {
  it('renders the page heading', () => {
    mockFetch.mockResolvedValue({ ok: true, json: async () => ACTIVE_SUB })
    render(<SubscriptionPage />)
    expect(screen.getByRole('heading', { name: /訂閱管理/ })).toBeInTheDocument()
  })

  it('shows loading indicator while fetching', () => {
    mockFetch.mockReturnValue(new Promise(() => {}))
    render(<SubscriptionPage />)
    expect(screen.getByText(/載入中/)).toBeInTheDocument()
  })

  it('shows plan name after fetch', async () => {
    mockFetch.mockResolvedValue({ ok: true, json: async () => ACTIVE_SUB })
    render(<SubscriptionPage />)
    await waitFor(() => expect(screen.getByText(/Pro/i)).toBeInTheDocument())
  })

  it('shows active status badge', async () => {
    mockFetch.mockResolvedValue({ ok: true, json: async () => ACTIVE_SUB })
    render(<SubscriptionPage />)
    await waitFor(() => expect(screen.getByText(/訂閱中/)).toBeInTheDocument())
  })

  it('shows trial badge and end date when trialing', async () => {
    mockFetch.mockResolvedValue({ ok: true, json: async () => TRIALING_SUB })
    render(<SubscriptionPage />)
    await waitFor(() => expect(screen.getByText(/試用中/)).toBeInTheDocument())
    expect(screen.getByText(/2026-06-23/)).toBeInTheDocument()
  })

  it('shows upgrade button when on free plan', async () => {
    mockFetch.mockResolvedValue({ ok: true, json: async () => TRIALING_SUB })
    render(<SubscriptionPage />)
    await waitFor(() =>
      expect(screen.getByRole('button', { name: /升級方案/ })).toBeInTheDocument()
    )
  })

  it('shows cancel button when on paid plan', async () => {
    mockFetch.mockResolvedValue({ ok: true, json: async () => ACTIVE_SUB })
    render(<SubscriptionPage />)
    await waitFor(() =>
      expect(screen.getByRole('button', { name: /取消訂閱/ })).toBeInTheDocument()
    )
  })

  it('calls cancel API when cancel button is clicked', async () => {
    mockFetch
      .mockResolvedValueOnce({ ok: true, json: async () => ACTIVE_SUB })
      .mockResolvedValueOnce({ ok: true, json: async () => ({}) })
    const user = userEvent.setup()
    render(<SubscriptionPage />)
    await waitFor(() =>
      expect(screen.getByRole('button', { name: /取消訂閱/ })).toBeInTheDocument()
    )
    await user.click(screen.getByRole('button', { name: /取消訂閱/ }))
    expect(mockFetch).toHaveBeenCalledWith(
      expect.stringContaining('/api/v1/subscription/cancel'),
      expect.objectContaining({ method: 'POST' })
    )
  })
})
