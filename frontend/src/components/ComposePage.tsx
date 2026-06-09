'use client'

import { useState } from 'react'
import { PostEditor } from './PostEditor'
import { PlatformSelector, Platform } from './PlatformSelector'
import { PublishPanel } from './PublishPanel'
import { ScheduleForm } from './ScheduleForm'

export function ComposePage() {
  const [content, setContent] = useState('')
  const [platforms, setPlatforms] = useState<Platform[]>([])

  return (
    <div className="flex flex-col gap-6">
      <PostEditor onContentChange={setContent} />
      <PlatformSelector selected={platforms} onChange={setPlatforms} />
      <div className="flex flex-col gap-4 rounded-xl border border-gray-100 bg-gray-50 p-4">
        <PublishPanel content={content} platforms={platforms} />
        <hr className="border-gray-200" />
        <ScheduleForm content={content} platforms={platforms} />
      </div>
    </div>
  )
}
