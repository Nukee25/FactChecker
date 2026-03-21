import React from 'react'

const STAGE_ICONS = {
  extracting: '📄',
  ai_detection: '🤖',
  claims_extracted: '🔍',
  verifying: '⚡',
  generating_report: '📊',
  complete: '✅',
}

export default function ProgressTracker({ stage, progress, message, currentClaim, totalClaims }) {
  const icon = STAGE_ICONS[stage] ?? '⏳'

  return (
    <div className="bg-gray-900 border border-gray-700 rounded-2xl p-6 shadow-xl space-y-4">
      <div className="flex items-center gap-3">
        <span className="text-2xl animate-pulse">{icon}</span>
        <div className="flex-1">
          <p className="text-white font-medium text-sm">{message || 'Processing...'}</p>
          {stage === 'verifying' && totalClaims > 0 && (
            <p className="text-blue-400 text-xs mt-0.5">
              Claim {currentClaim} of {totalClaims}
            </p>
          )}
        </div>
        <span className="text-blue-400 font-bold text-sm">{progress}%</span>
      </div>

      {/* Progress bar */}
      <div className="w-full bg-gray-800 rounded-full h-2.5">
        <div
          className="bg-blue-500 h-2.5 rounded-full transition-all duration-500"
          style={{ width: `${progress}%` }}
        />
      </div>

      {/* Stage steps */}
      <div className="flex justify-between text-xs text-gray-500 pt-1">
        {Object.entries(STAGE_ICONS).map(([s, ico]) => (
          <span
            key={s}
            className={`transition-colors ${stage === s ? 'text-blue-400 font-semibold' : ''}`}
            title={s}
          >
            {ico}
          </span>
        ))}
      </div>
    </div>
  )
}
