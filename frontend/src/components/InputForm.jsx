import React, { useRef } from 'react'

export default function InputForm({ input, setInput, inputType, setInputType, onVerify, onCheckMedia, isLoading, mediaFile, setMediaFile }) {
  const fileInputRef = useRef(null)

  const handleFileChange = (e) => {
    const file = e.target.files?.[0] || null
    setMediaFile(file)
    if (file) setInput(file.name)
  }

  const handleTypeChange = (type) => {
    setInputType(type)
    setInput('')
    setMediaFile(null)
    if (fileInputRef.current) fileInputRef.current.value = ''
  }

  const isMediaMode = inputType === 'image'
  const canSubmit = !isLoading && (isMediaMode ? (mediaFile || input.trim()) : input.trim())

  const handleUrlChange = (e) => {
    setInput(e.target.value)
    setMediaFile(null)
  }

  return (
    <div className="bg-gray-900 border border-gray-700 rounded-2xl p-6 shadow-xl space-y-4">
      {/* Mode toggle */}
      <div className="flex gap-2">
        {[
          { id: 'text', label: '📝 Text' },
          { id: 'url', label: '🔗 URL' },
          { id: 'image', label: '🖼️ Image' },
        ].map(({ id, label }) => (
          <button
            key={id}
            onClick={() => handleTypeChange(id)}
            className={`px-5 py-2 rounded-lg font-medium text-sm transition-colors ${
              inputType === id
                ? 'bg-blue-600 text-white shadow-md'
                : 'bg-gray-800 text-gray-400 hover:bg-gray-700'
            }`}
          >
            {label}
          </button>
        ))}
      </div>

      {/* Input field */}
      {inputType === 'text' && (
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Enter article text, news, or any content to fact-check..."
          rows={7}
          className="w-full bg-gray-800 border border-gray-600 rounded-xl px-4 py-3 text-gray-100 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none text-sm"
        />
      )}

      {inputType === 'url' && (
        <input
          type="url"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="https://example.com/article"
          className="w-full bg-gray-800 border border-gray-600 rounded-xl px-4 py-3 text-gray-100 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
        />
      )}

      {inputType === 'image' && (
        <div className="space-y-3">
          <div
            className="border-2 border-dashed border-gray-600 rounded-xl p-6 text-center cursor-pointer hover:border-blue-500 transition-colors"
            onClick={() => fileInputRef.current?.click()}
          >
            {mediaFile ? (
              <p className="text-gray-300 text-sm">{mediaFile.name}</p>
            ) : (
              <>
                <p className="text-gray-400 text-sm">Click to upload an image</p>
                <p className="text-gray-600 text-xs mt-1">PNG, JPG, WEBP, GIF supported</p>
              </>
            )}
          </div>
          <input
            ref={fileInputRef}
            type="file"
            accept="image/*"
            className="hidden"
            onChange={handleFileChange}
          />
          <div className="flex items-center gap-2">
            <div className="flex-1 h-px bg-gray-700" />
            <span className="text-gray-500 text-xs">or paste an image URL</span>
            <div className="flex-1 h-px bg-gray-700" />
          </div>
          <input
            type="url"
            value={mediaFile ? '' : input}
            onChange={handleUrlChange}
            placeholder="https://example.com/image.jpg"
            disabled={!!mediaFile}
            className="w-full bg-gray-800 border border-gray-600 rounded-xl px-4 py-3 text-gray-100 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm disabled:opacity-40"
          />
        </div>
      )}

      {/* Submit button */}
      <button
        onClick={isMediaMode ? onCheckMedia : onVerify}
        disabled={!canSubmit}
        className="w-full py-3 rounded-xl font-semibold text-white bg-blue-600 hover:bg-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center justify-center gap-2"
      >
        {isLoading ? (
          <>
            <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24" fill="none">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z" />
            </svg>
            {isMediaMode ? 'Analyzing...' : 'Verifying...'}
          </>
        ) : isMediaMode ? (
          '🔍 Check Media Authenticity'
        ) : (
          '✅ Verify Facts'
        )}
      </button>
    </div>
  )
}
