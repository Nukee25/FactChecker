import React from 'react'
import ClaimCard from './ClaimCard'

function scoreColor(score) {
  if (score >= 70) return 'text-green-400'
  if (score >= 40) return 'text-yellow-400'
  return 'text-red-400'
}

function scoreRingColor(score) {
  if (score >= 70) return '#22c55e'
  if (score >= 40) return '#eab308'
  return '#ef4444'
}

export default function AccuracyReport({ report }) {
  const score = report.overall_score ?? 0
  const ai = report.ai_detection || {}

  const circumference = 2 * Math.PI * 45
  const offset = circumference - (score / 100) * circumference

  return (
    <div className="space-y-6">
      {/* Score + stats */}
      <div className="bg-gray-900 border border-gray-700 rounded-2xl p-6 shadow-xl">
        <h2 className="text-lg font-bold text-white mb-6">Accuracy Report</h2>

        <div className="flex flex-col sm:flex-row items-center gap-8">
          {/* Circular score */}
          <div className="flex flex-col items-center">
            <svg width="120" height="120" viewBox="0 0 120 120">
              <circle cx="60" cy="60" r="45" fill="none" stroke="#1f2937" strokeWidth="10" />
              <circle
                cx="60"
                cy="60"
                r="45"
                fill="none"
                stroke={scoreRingColor(score)}
                strokeWidth="10"
                strokeDasharray={circumference}
                strokeDashoffset={offset}
                strokeLinecap="round"
                transform="rotate(-90 60 60)"
                style={{ transition: 'stroke-dashoffset 1s ease' }}
              />
            </svg>
            <p className={`text-4xl font-bold -mt-16 ${scoreColor(score)}`}>{score}%</p>
            <p className="text-gray-400 text-sm mt-6">Overall Score</p>
          </div>

          {/* Stats grid */}
          <div className="grid grid-cols-2 gap-3 flex-1 w-full">
            {[
              { label: 'True', value: report.true_count, color: 'bg-green-900/50 border-green-700 text-green-400' },
              { label: 'False', value: report.false_count, color: 'bg-red-900/50 border-red-700 text-red-400' },
              { label: 'Partially True', value: report.partial_count, color: 'bg-yellow-900/50 border-yellow-700 text-yellow-400' },
              { label: 'Unverifiable', value: report.unverifiable_count, color: 'bg-gray-800 border-gray-600 text-gray-400' },
            ].map(({ label, value, color }) => (
              <div key={label} className={`border rounded-xl p-3 text-center ${color}`}>
                <p className="text-2xl font-bold">{value}</p>
                <p className="text-xs mt-0.5 opacity-80">{label}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* AI Detection */}
      {ai && (
        <div className="bg-gray-900 border border-gray-700 rounded-2xl p-6 shadow-xl space-y-4">
          <h2 className="text-lg font-bold text-white">🤖 AI Detection</h2>

          <div className="space-y-3">
            <div>
              <div className="flex justify-between text-sm text-gray-400 mb-1">
                <span>AI-Generated Probability</span>
                <span className="text-blue-400 font-medium">{ai.ai_probability ?? 0}%</span>
              </div>
              <div className="w-full bg-gray-800 rounded-full h-2">
                <div
                  className="bg-blue-500 h-2 rounded-full transition-all duration-700"
                  style={{ width: `${ai.ai_probability ?? 0}%` }}
                />
              </div>
            </div>

            <div>
              <div className="flex justify-between text-sm text-gray-400 mb-1">
                <span>Human-Written Probability</span>
                <span className="text-green-400 font-medium">{ai.human_probability ?? 0}%</span>
              </div>
              <div className="w-full bg-gray-800 rounded-full h-2">
                <div
                  className="bg-green-500 h-2 rounded-full transition-all duration-700"
                  style={{ width: `${ai.human_probability ?? 0}%` }}
                />
              </div>
            </div>
          </div>

          {(ai.indicators || []).length > 0 && (
            <div>
              <p className="text-xs text-gray-500 uppercase tracking-wide mb-2">Indicators</p>
              <ul className="space-y-1">
                {ai.indicators.map((ind, i) => (
                  <li key={i} className="text-gray-300 text-sm flex items-start gap-2">
                    <span className="text-gray-600 mt-0.5">•</span>
                    {ind}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}

      {/* Verified Claims */}
      <div className="space-y-4">
        <h2 className="text-lg font-bold text-white">Verified Claims ({report.total_claims})</h2>
        {(report.claims || []).map((claim_result, i) => (
          <ClaimCard key={i} claim_result={claim_result} index={i} />
        ))}
      </div>
    </div>
  )
}
