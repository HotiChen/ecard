import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { NavBar } from '../NavBar'

describe('NavBar', () => {
  it('renders all navigation links', () => {
    render(<NavBar active="compose" onNavigate={() => {}} />)
    expect(screen.getByRole('button', { name: /發文/ })).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /排程/ })).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /數據/ })).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /訂閱/ })).toBeInTheDocument()
  })

  it('marks active tab with aria-current', () => {
    render(<NavBar active="schedule" onNavigate={() => {}} />)
    expect(screen.getByRole('button', { name: /排程/ })).toHaveAttribute('aria-current', 'page')
  })

  it('does not mark inactive tabs', () => {
    render(<NavBar active="compose" onNavigate={() => {}} />)
    expect(screen.getByRole('button', { name: /排程/ })).not.toHaveAttribute('aria-current', 'page')
  })

  it('calls onNavigate with correct tab when clicked', async () => {
    const user = userEvent.setup()
    const handler = vi.fn()
    render(<NavBar active="compose" onNavigate={handler} />)
    await user.click(screen.getByRole('button', { name: /排程/ }))
    expect(handler).toHaveBeenCalledWith('schedule')
  })

  it('calls onNavigate with analytics tab', async () => {
    const user = userEvent.setup()
    const handler = vi.fn()
    render(<NavBar active="compose" onNavigate={handler} />)
    await user.click(screen.getByRole('button', { name: /數據/ }))
    expect(handler).toHaveBeenCalledWith('analytics')
  })
})
