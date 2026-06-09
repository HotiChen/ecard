'use client'

import { Component, ReactNode, ErrorInfo } from 'react'

interface Props {
  children: ReactNode
}

interface State {
  hasError: boolean
  error: Error | null
}

export class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props)
    this.state = { hasError: false, error: null }
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error }
  }

  componentDidCatch(error: Error, info: ErrorInfo) {
    console.error('ErrorBoundary caught:', error, info)
  }

  handleRetry = () => {
    this.setState({ hasError: false, error: null })
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="rounded-xl border border-red-200 bg-red-50 p-6 flex flex-col gap-3">
          <h2 className="text-lg font-semibold text-red-700">發生錯誤</h2>
          <p className="text-sm text-red-600 font-mono">
            {this.state.error?.message ?? '未知錯誤'}
          </p>
          <button
            onClick={this.handleRetry}
            className="self-start rounded-lg border border-red-300 px-4 py-1.5 text-sm font-medium text-red-700 hover:bg-red-100"
          >
            重試
          </button>
        </div>
      )
    }
    return this.props.children
  }
}
