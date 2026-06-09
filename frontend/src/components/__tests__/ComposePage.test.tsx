import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { ComposePage } from '../ComposePage'

const mockFetch = vi.fn()
vi.stubGlobal('fetch', mockFetch)

afterEach(() => {
  vi.clearAllMocks()
})

describe('ComposePage — 發文頁整合', () => {
  it('renders the post editor textarea', () => {
    render(<ComposePage />)
    expect(screen.getByRole('textbox')).toBeInTheDocument()
  })

  it('renders all three platform checkboxes', () => {
    render(<ComposePage />)
    expect(screen.getByRole('checkbox', { name: /Threads/ })).toBeInTheDocument()
    expect(screen.getByRole('checkbox', { name: /Instagram/ })).toBeInTheDocument()
    expect(screen.getByRole('checkbox', { name: /X \(Twitter\)/ })).toBeInTheDocument()
  })

  it('renders the publish button', () => {
    render(<ComposePage />)
    expect(screen.getByRole('button', { name: /發布/ })).toBeInTheDocument()
  })

  it('renders the schedule button', () => {
    render(<ComposePage />)
    expect(screen.getByRole('button', { name: /建立排程/ })).toBeInTheDocument()
  })

  it('publish button is disabled when no content and no platform', () => {
    render(<ComposePage />)
    expect(screen.getByRole('button', { name: /發布/ })).toBeDisabled()
  })

  it('enables publish button after typing content and selecting a platform', async () => {
    mockFetch.mockResolvedValue({ ok: true, json: async () => ({}) })
    const user = userEvent.setup()
    render(<ComposePage />)
    await user.type(screen.getByRole('textbox'), '測試貼文內容')
    await user.click(screen.getByRole('checkbox', { name: /Threads/ }))
    expect(screen.getByRole('button', { name: /發布/ })).not.toBeDisabled()
  })
})
