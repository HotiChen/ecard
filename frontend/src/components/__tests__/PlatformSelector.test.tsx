import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { PlatformSelector } from '../PlatformSelector'

describe('PlatformSelector', () => {
  it('renders all three platforms', () => {
    render(<PlatformSelector selected={[]} onChange={() => {}} />)
    expect(screen.getByText('Threads')).toBeInTheDocument()
    expect(screen.getByText('Instagram')).toBeInTheDocument()
    expect(screen.getByText('X (Twitter)')).toBeInTheDocument()
  })

  it('checks the pre-selected platforms', () => {
    render(<PlatformSelector selected={['threads']} onChange={() => {}} />)
    expect(screen.getByRole('checkbox', { name: /Threads/ })).toBeChecked()
    expect(screen.getByRole('checkbox', { name: /Instagram/ })).not.toBeChecked()
  })

  it('calls onChange when a platform is toggled on', async () => {
    const user = userEvent.setup()
    const handler = vi.fn()
    render(<PlatformSelector selected={[]} onChange={handler} />)
    await user.click(screen.getByRole('checkbox', { name: /Threads/ }))
    expect(handler).toHaveBeenCalledWith(['threads'])
  })

  it('calls onChange when a platform is toggled off', async () => {
    const user = userEvent.setup()
    const handler = vi.fn()
    render(<PlatformSelector selected={['threads', 'instagram']} onChange={handler} />)
    await user.click(screen.getByRole('checkbox', { name: /Threads/ }))
    expect(handler).toHaveBeenCalledWith(['instagram'])
  })

  it('allows multiple platforms to be selected', async () => {
    const user = userEvent.setup()
    const handler = vi.fn()
    render(<PlatformSelector selected={[]} onChange={handler} />)
    await user.click(screen.getByRole('checkbox', { name: /Threads/ }))
    await user.click(screen.getByRole('checkbox', { name: /Instagram/ }))
    expect(handler).toHaveBeenLastCalledWith(['instagram'])
  })
})
