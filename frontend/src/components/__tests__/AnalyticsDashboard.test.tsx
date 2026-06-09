import { render, screen, waitFor } from '@testing-library/react'
import { AnalyticsDashboard } from '../AnalyticsDashboard'

const mockFetch = vi.fn()
vi.stubGlobal('fetch', mockFetch)

afterEach(() => {
  vi.clearAllMocks()
})

const METRICS = [
  {
    post_id: 1,
    platform: 'threads',
    likes: 120,
    comments: 30,
    replies: 10,
    reposts: 5,
    views: 1000,
  },
  {
    post_id: 2,
    platform: 'instagram',
    likes: 80,
    comments: 20,
    replies: 5,
    reposts: 2,
    views: 500,
  },
]

describe('AnalyticsDashboard — 數據看板', () => {
  it('renders the page heading', () => {
    mockFetch.mockResolvedValue({ ok: true, json: async () => [] })
    render(<AnalyticsDashboard />)
    expect(screen.getByRole('heading', { name: /數據看板/ })).toBeInTheDocument()
  })

  it('shows loading indicator while fetching', () => {
    mockFetch.mockReturnValue(new Promise(() => {}))
    render(<AnalyticsDashboard />)
    expect(screen.getByText(/載入中/)).toBeInTheDocument()
  })

  it('shows total likes after fetch', async () => {
    mockFetch.mockResolvedValue({ ok: true, json: async () => METRICS })
    render(<AnalyticsDashboard />)
    await waitFor(() => expect(screen.getByText('200')).toBeInTheDocument())
  })

  it('shows total comments after fetch', async () => {
    mockFetch.mockResolvedValue({ ok: true, json: async () => METRICS })
    render(<AnalyticsDashboard />)
    await waitFor(() => expect(screen.getByText('50')).toBeInTheDocument())
  })

  it('shows total views after fetch', async () => {
    mockFetch.mockResolvedValue({ ok: true, json: async () => METRICS })
    render(<AnalyticsDashboard />)
    await waitFor(() => expect(screen.getByText('1500')).toBeInTheDocument())
  })

  it('shows empty state when no metrics', async () => {
    mockFetch.mockResolvedValue({ ok: true, json: async () => [] })
    render(<AnalyticsDashboard />)
    await waitFor(() =>
      expect(screen.getByText(/尚無數據/)).toBeInTheDocument()
    )
  })

  it('displays a summary label for likes', async () => {
    mockFetch.mockResolvedValue({ ok: true, json: async () => METRICS })
    render(<AnalyticsDashboard />)
    await waitFor(() =>
      expect(screen.getByText(/按讚數/)).toBeInTheDocument()
    )
  })
})
