'use client'

import { useState } from 'react'

const MAX_CHARS = 5000

interface PostEditorProps {
  onContentChange: (content: string) => void
}

export function PostEditor({ onContentChange }: PostEditorProps) {
  const [content, setContent] = useState('')

  function handleChange(e: React.ChangeEvent<HTMLTextAreaElement>) {
    const val = e.target.value
    setContent(val)
    onContentChange(val)
  }

  const overLimit = content.length > MAX_CHARS

  return (
    <div className="flex flex-col gap-2">
      <textarea
        className={`w-full rounded-lg border p-3 text-sm resize-none min-h-[160px] focus:outline-none focus:ring-2 ${
          overLimit ? 'border-red-500 focus:ring-red-400' : 'border-gray-300 focus:ring-blue-400'
        }`}
        placeholder="輸入貼文內容（支援 Threads、Instagram、X）"
        value={content}
        onChange={handleChange}
        rows={6}
      />
      <div className="flex justify-between text-xs text-gray-500">
        <span>
          {overLimit && (
            <span className="text-red-500 font-medium">超過 5000 字元限制　</span>
          )}
        </span>
        <span className={overLimit ? 'text-red-500' : ''}>
          {content.length} / {MAX_CHARS}
        </span>
      </div>
    </div>
  )
}
