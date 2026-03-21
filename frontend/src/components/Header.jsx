import React from 'react'

export default function Header() {
  return (
    <header className="bg-gradient-to-r from-blue-900 to-indigo-900 shadow-lg">
      <div className="max-w-4xl mx-auto px-4 py-6 flex items-center gap-4">
        <div className="flex-shrink-0 text-4xl select-none" aria-hidden="true">
          🛡️
        </div>
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-white">FactChecker</h1>
          <p className="text-blue-200 text-sm mt-0.5">AI-powered claim verification</p>
        </div>
      </div>
    </header>
  )
}
