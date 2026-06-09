import { render, screen, fireEvent } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { PostEditor } from '../PostEditor'

describe('PostEditor', () => {
  it('renders a textarea', () => {
    render(<PostEditor onContentChange={() => {}} />)
    expect(screen.getByRole('textbox')).toBeInTheDocument()
  })

  it('shows character count', () => {
    render(<PostEditor onContentChange={() => {}} />)
    expect(screen.getByText(/0 \/ 5000/)).toBeInTheDocument()
  })

  it('updates character count as user types', async () => {
    const user = userEvent.setup()
    render(<PostEditor onContentChange={() => {}} />)
    await user.type(screen.getByRole('textbox'), 'hello')
    expect(screen.getByText(/5 \/ 5000/)).toBeInTheDocument()
  })

  it('calls onContentChange with current value', async () => {
    const user = userEvent.setup()
    const handler = vi.fn()
    render(<PostEditor onContentChange={handler} />)
    await user.type(screen.getByRole('textbox'), 'hi')
    expect(handler).toHaveBeenLastCalledWith('hi')
  })

  it('shows error when content exceeds 5000 chars', () => {
    render(<PostEditor onContentChange={() => {}} />)
    fireEvent.change(screen.getByRole('textbox'), {
      target: { value: 'a'.repeat(5001) },
    })
    expect(screen.getByText(/超過 5000 字元限制/)).toBeInTheDocument()
  })

  it('shows placeholder text', () => {
    render(<PostEditor onContentChange={() => {}} />)
    expect(screen.getByPlaceholderText(/輸入貼文內容/)).toBeInTheDocument()
  })
})
