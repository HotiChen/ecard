import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { AiAnalysisPage } from '../AiAnalysisPage'

const mockFetch = vi.fn()
vi.stubGlobal('fetch', mockFetch)

afterEach(() => {
  vi.clearAllMocks()
})

describe('AiAnalysisPage — AI 分析', () => {
  it('renders page heading', () => {
    render(<AiAnalysisPage />)
    expect(screen.getByRole('heading', { name: /AI 分析/ })).toBeInTheDocument()
  })

  it('renders sentiment analysis section', () => {
    render(<AiAnalysisPage />)
    expect(screen.getByText(/留言情緒分析/)).toBeInTheDocument()
  })

  it('renders weekly report section', () => {
    render(<AiAnalysisPage />)
    expect(screen.getByText(/每週週報/)).toBeInTheDocument()
  })

  it('renders next post suggestion section', () => {
    render(<AiAnalysisPage />)
    expect(screen.getByText(/下一篇建議/)).toBeInTheDocument()
  })

  it('can type a comment in the sentiment input', async () => {
    const user = userEvent.setup()
    render(<AiAnalysisPage />)
    const input = screen.getByPlaceholderText(/輸入留言/)
    await user.type(input, '這照片太棒了！')
    expect(input).toHaveValue('這照片太棒了！')
  })

  it('calls sentiment API and shows result', async () => {
    mockFetch.mockResolvedValue({
      ok: true,
      json: async () => [{ comment: '好棒！', label: 'positive' }],
    })
    const user = userEvent.setup()
    render(<AiAnalysisPage />)
    await user.type(screen.getByPlaceholderText(/輸入留言/), '好棒！')
    await user.click(screen.getByRole('button', { name: /分析情緒/ }))
    await waitFor(() =>
      expect(screen.getByText(/positive/)).toBeInTheDocument()
    )
  })

  it('calls suggest API and shows suggestion', async () => {
    mockFetch.mockResolvedValue({
      ok: true,
      json: async () => ({ suggestion: '建議主題：夜間攝影技巧' }),
    })
    const user = userEvent.setup()
    render(<AiAnalysisPage />)
    await user.click(screen.getByRole('button', { name: /取得建議/ }))
    await waitFor(() =>
      expect(screen.getByText(/夜間攝影技巧/)).toBeInTheDocument()
    )
  })

  it('shows loading state during sentiment analysis', async () => {
    mockFetch.mockReturnValue(new Promise(() => {}))
    const user = userEvent.setup()
    render(<AiAnalysisPage />)
    await user.type(screen.getByPlaceholderText(/輸入留言/), '好棒')
    await user.click(screen.getByRole('button', { name: /分析情緒/ }))
    expect(screen.getByText(/分析中/)).toBeInTheDocument()
  })
})
