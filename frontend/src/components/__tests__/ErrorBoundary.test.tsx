import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { ErrorBoundary } from '../ErrorBoundary'

// Suppress console.error for expected errors in tests
const originalError = console.error
beforeEach(() => {
  console.error = vi.fn()
})
afterEach(() => {
  console.error = originalError
})

function Bomb({ shouldThrow }: { shouldThrow: boolean }) {
  if (shouldThrow) throw new Error('Test error: component crashed')
  return <p>正常顯示</p>
}

describe('ErrorBoundary', () => {
  it('renders children when no error', () => {
    render(
      <ErrorBoundary>
        <Bomb shouldThrow={false} />
      </ErrorBoundary>
    )
    expect(screen.getByText('正常顯示')).toBeInTheDocument()
  })

  it('renders fallback UI when child throws', () => {
    render(
      <ErrorBoundary>
        <Bomb shouldThrow={true} />
      </ErrorBoundary>
    )
    expect(screen.getByText(/發生錯誤/)).toBeInTheDocument()
  })

  it('shows error message in fallback', () => {
    render(
      <ErrorBoundary>
        <Bomb shouldThrow={true} />
      </ErrorBoundary>
    )
    expect(screen.getByText(/Test error/)).toBeInTheDocument()
  })

  it('shows a retry button in fallback', () => {
    render(
      <ErrorBoundary>
        <Bomb shouldThrow={true} />
      </ErrorBoundary>
    )
    expect(screen.getByRole('button', { name: /重試/ })).toBeInTheDocument()
  })

  it('renders children again after retry click', async () => {
    const user = userEvent.setup()
    // Wrapper holds state so shouldThrow can be updated before the boundary re-renders
    let setShouldThrow: (v: boolean) => void
    function Wrapper() {
      const [shouldThrow, setFlag] = (setShouldThrow = (v: boolean) => setFlag(v), [true, (v: boolean) => setFlag(v)])
      return <ErrorBoundary><Bomb shouldThrow={shouldThrow} /></ErrorBoundary>
    }

    // Simpler: use a controlled parent via rerender order
    // Fix the child first, then click retry
    const { rerender } = render(
      <ErrorBoundary key="eb">
        <Bomb shouldThrow={true} />
      </ErrorBoundary>
    )
    expect(screen.getByText(/發生錯誤/)).toBeInTheDocument()

    // Provide a non-throwing child THEN click retry to reset boundary state
    rerender(
      <ErrorBoundary key="eb">
        <Bomb shouldThrow={false} />
      </ErrorBoundary>
    )
    await user.click(screen.getByRole('button', { name: /重試/ }))
    expect(screen.getByText('正常顯示')).toBeInTheDocument()
  })
})
