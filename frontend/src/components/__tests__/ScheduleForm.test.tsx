import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { ScheduleForm } from '../ScheduleForm'

const mockFetch = vi.fn()
vi.stubGlobal('fetch', mockFetch)

afterEach(() => {
  vi.clearAllMocks()
})

describe('ScheduleForm — 排程發文表單', () => {
  it('renders a datetime input', () => {
    render(<ScheduleForm content="測試貼文" platforms={['threads']} />)
    expect(screen.getByLabelText(/排程時間/)).toBeInTheDocument()
  })

  it('renders a submit button', () => {
    render(<ScheduleForm content="測試貼文" platforms={['threads']} />)
    expect(screen.getByRole('button', { name: /建立排程/ })).toBeInTheDocument()
  })

  it('disables submit when no content', () => {
    render(<ScheduleForm content="" platforms={['threads']} />)
    expect(screen.getByRole('button', { name: /建立排程/ })).toBeDisabled()
  })

  it('disables submit when no platform selected', () => {
    render(<ScheduleForm content="測試" platforms={[]} />)
    expect(screen.getByRole('button', { name: /建立排程/ })).toBeDisabled()
  })

  it('disables submit when no datetime selected', async () => {
    render(<ScheduleForm content="測試" platforms={['threads']} />)
    expect(screen.getByRole('button', { name: /建立排程/ })).toBeDisabled()
  })

  it('calls POST /api/v1/schedules on submit', async () => {
    mockFetch.mockResolvedValue({ ok: true, json: async () => ({ id: 42 }) })
    const user = userEvent.setup()
    render(<ScheduleForm content="排程測試" platforms={['threads']} />)
    await user.type(screen.getByLabelText(/排程時間/), '2026-07-01T09:00')
    await user.click(screen.getByRole('button', { name: /建立排程/ }))
    expect(mockFetch).toHaveBeenCalledWith(
      expect.stringContaining('/api/v1/schedules'),
      expect.objectContaining({ method: 'POST' })
    )
  })

  it('shows success message after schedule created', async () => {
    mockFetch.mockResolvedValue({ ok: true, json: async () => ({ id: 42 }) })
    const user = userEvent.setup()
    render(<ScheduleForm content="排程測試" platforms={['threads']} />)
    await user.type(screen.getByLabelText(/排程時間/), '2026-07-01T09:00')
    await user.click(screen.getByRole('button', { name: /建立排程/ }))
    await waitFor(() =>
      expect(screen.getByText(/排程已建立/)).toBeInTheDocument()
    )
  })

  it('shows error message on failure', async () => {
    mockFetch.mockResolvedValue({ ok: false, json: async () => ({}) })
    const user = userEvent.setup()
    render(<ScheduleForm content="排程測試" platforms={['threads']} />)
    await user.type(screen.getByLabelText(/排程時間/), '2026-07-01T09:00')
    await user.click(screen.getByRole('button', { name: /建立排程/ }))
    await waitFor(() =>
      expect(screen.getByText(/排程失敗/)).toBeInTheDocument()
    )
  })
})
