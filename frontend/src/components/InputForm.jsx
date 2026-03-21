import React from 'react'

export default function InputForm({ input, setInput, inputType, setInputType, onVerify, isLoading }) {
  return (
    <div className="bg-gray-900 border border-gray-700 rounded-2xl p-6 shadow-xl space-y-4">
      {/* Mode toggle */}
      <div className="flex gap-2">
        {['text', 'url'].map((type) => (
          <button
            key={type}
            onClick={() => setInputType(type)}
            className={`px-5 py-2 rounded-lg font-medium text-sm transition-colors ${
              inputType === type
                ? 'bg-blue-600 text-white shadow-md'
                : 'bg-gray-800 text-gray-400 hover:bg-gray-700'
            }`}
          >
            {type === 'text' ? '📝 Text' : '🔗 URL'}
          </button>
        ))}
      </div>

      {/* Input field */}
      {inputType === 'text' ? (
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Enter article text, news, or any content to fact-check..."
          rows={7}
          className="w-full bg-gray-800 border border-gray-600 rounded-xl px-4 py-3 text-gray-100 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none text-sm"
        />
      ) : (
        <input
          type="url"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="https://example.com/article"
          className="w-full bg-gray-800 border border-gray-600 rounded-xl px-4 py-3 text-gray-100 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
        />
      )}

      {/* Submit button */}
      <button
        onClick={onVerify}
        disabled={isLoading || !input.trim()}
        className="w-full py-3 rounded-xl font-semibold text-white bg-blue-600 hover:bg-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center justify-center gap-2"
      >
        {isLoading ? (
          <>
            <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24" fill="none">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z" />
            </svg>
            Verifying...
          </>
        ) : (
          '✅ Verify Facts'
        )}
      </button>
    </div>
  )
}
