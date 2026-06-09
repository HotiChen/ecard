import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { SchedulePage } from '../SchedulePage'

const mockFetch = vi.fn()
vi.stubGlobal('fetch', mockFetch)

afterEach(() => {
  vi.clearAllMocks()
})

const SCHEDULED_POSTS = [
  {
    id: 1,
    content: '攝影日記第一篇',
    platforms: ['threads'],
    scheduled_at: '2026-06-15T09:00:00Z',
    is_canceled: false,
    executed_at: null,
  },
  {
    id: 2,
    content: '攝影日記第二篇',
    platforms: ['instagram', 'threads'],
    scheduled_at: '2026-06-16T10:00:00Z',
    is_canceled: true,
    executed_at: null,
  },
]

const EXECUTED_POST = {
  id: 3,
  content: '夜景攝影特輯',
  platforms: ['threads'],
  scheduled_at: '2026-06-14T08:00:00Z',
  is_canceled: false,
  executed_at: '2026-06-14T08:01:00Z',
}

describe('SchedulePage — 排程任務管理', () => {
  it('renders the page heading', () => {
    mockFetch.mockResolvedValue({ ok: true, json: async () => [] })
    render(<SchedulePage />)
    expect(screen.getByRole('heading', { name: /排程管理/ })).toBeInTheDocument()
  })

  it('shows a loading indicator while fetching', () => {
    mockFetch.mockReturnValue(new Promise(() => {}))
    render(<SchedulePage />)
    expect(screen.getByText(/載入中/)).toBeInTheDocument()
  })

  it('lists scheduled posts after fetch', async () => {
    mockFetch.mockResolvedValue({
      ok: true,
      json: async () => SCHEDULED_POSTS,
    })
    render(<SchedulePage />)
    await waitFor(() =>
      expect(screen.getByText(/攝影日記第一篇/)).toBeInTheDocument()
    )
    expect(screen.getByText(/攝影日記第二篇/)).toBeInTheDocument()
  })

  it('shows empty state when no scheduled posts', async () => {
    mockFetch.mockResolvedValue({ ok: true, json: async () => [] })
    render(<SchedulePage />)
    await waitFor(() =>
      expect(screen.getByText(/目前沒有排程貼文/)).toBeInTheDocument()
    )
  })

  it('shows canceled badge for canceled posts', async () => {
    mockFetch.mockResolvedValue({
      ok: true,
      json: async () => SCHEDULED_POSTS,
    })
    render(<SchedulePage />)
    await waitFor(() =>
      expect(screen.getByText(/已取消/)).toBeInTheDocument()
    )
  })

  it('shows executed badge for executed posts', async () => {
    mockFetch.mockResolvedValue({ ok: true, json: async () => [EXECUTED_POST] })
    render(<SchedulePage />)
    await waitFor(() =>
      expect(screen.getByText(/已發布/)).toBeInTheDocument()
    )
  })

  it('renders a refresh button', async () => {
    mockFetch.mockResolvedValue({ ok: true, json: async () => [] })
    render(<SchedulePage />)
    await waitFor(() =>
      expect(screen.getByRole('button', { name: /重新整理/ })).toBeInTheDocument()
    )
  })

  it('re-fetches list when refresh button is clicked', async () => {
    mockFetch.mockResolvedValue({ ok: true, json: async () => [] })
    const user = userEvent.setup()
    render(<SchedulePage />)
    await waitFor(() =>
      expect(screen.getByRole('button', { name: /重新整理/ })).toBeInTheDocument()
    )
    await user.click(screen.getByRole('button', { name: /重新整理/ }))
    expect(mockFetch).toHaveBeenCalledTimes(2)
  })

  it('calls cancel API when cancel button is clicked', async () => {
    mockFetch
      .mockResolvedValueOnce({ ok: true, json: async () => SCHEDULED_POSTS })
      .mockResolvedValueOnce({ ok: true, json: async () => ({}) })
    const user = userEvent.setup()
    render(<SchedulePage />)
    await waitFor(() =>
      expect(screen.getByText(/攝影日記第一篇/)).toBeInTheDocument()
    )
    await user.click(screen.getAllByRole('button', { name: /取消/ })[0])
    expect(mockFetch).toHaveBeenCalledWith(
      expect.stringContaining('/api/v1/schedules/1/cancel'),
      expect.objectContaining({ method: 'POST' })
    )
  })
})
