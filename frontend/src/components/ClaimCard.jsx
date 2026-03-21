import React, { useState } from 'react'

const VERDICT_STYLES = {
  True: { border: 'border-green-500', badge: 'bg-green-700 text-green-100', bar: 'bg-green-500' },
  False: { border: 'border-red-500', badge: 'bg-red-700 text-red-100', bar: 'bg-red-500' },
  'Partially True': { border: 'border-yellow-500', badge: 'bg-yellow-700 text-yellow-100', bar: 'bg-yellow-500' },
  Unverifiable: { border: 'border-gray-500', badge: 'bg-gray-700 text-gray-300', bar: 'bg-gray-500' },
}

export default function ClaimCard({ claim_result, index }) {
  const [expanded, setExpanded] = useState(false)
  const verdict = claim_result.verdict || 'Unverifiable'
  const styles = VERDICT_STYLES[verdict] || VERDICT_STYLES.Unverifiable
  const confidence = claim_result.confidence ?? 0
  const evidence = claim_result.evidence || []

  return (
    <div className={`bg-gray-900 border-l-4 ${styles.border} border border-gray-700 rounded-xl p-5 space-y-3`}>
      {/* Header */}
      <div className="flex items-start justify-between gap-3">
        <div className="flex items-start gap-2 flex-1">
          <span className="text-gray-500 font-mono text-sm mt-0.5">#{index + 1}</span>
          <p className="text-gray-100 text-sm font-medium leading-relaxed">{claim_result.claim}</p>
        </div>
        <span className={`shrink-0 px-3 py-1 rounded-full text-xs font-bold ${styles.badge}`}>
          {verdict}
        </span>
      </div>

      {/* Confidence bar */}
      <div>
        <div className="flex justify-between text-xs text-gray-400 mb-1">
          <span>Confidence</span>
          <span>{confidence}%</span>
        </div>
        <div className="w-full bg-gray-800 rounded-full h-1.5">
          <div
            className={`${styles.bar} h-1.5 rounded-full transition-all duration-500`}
            style={{ width: `${confidence}%` }}
          />
        </div>
      </div>

      {/* Reasoning (collapsible) */}
      <div>
        <button
          onClick={() => setExpanded((p) => !p)}
          className="text-xs text-blue-400 hover:text-blue-300 transition-colors"
        >
          {expanded ? '▲ Hide reasoning' : '▼ Show reasoning'}
        </button>
        {expanded && (
          <p className="mt-2 text-gray-300 text-sm leading-relaxed">{claim_result.reasoning}</p>
        )}
      </div>

      {/* Source counts */}
      <div className="flex gap-4 text-xs">
        <span className="text-green-400">
          ✔ {(claim_result.supporting_sources || []).length} supporting
        </span>
        <span className="text-red-400">
          ✖ {(claim_result.conflicting_sources || []).length} conflicting
        </span>
      </div>

      {/* Evidence list */}
      {evidence.length > 0 && (
        <div className="space-y-2 pt-1">
          <p className="text-xs text-gray-500 uppercase tracking-wide">Sources</p>
          {evidence.map((e, i) => (
            <div key={i} className="bg-gray-800 rounded-lg p-3 space-y-1">
              <a
                href={e.url}
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue-400 hover:text-blue-300 text-xs font-medium line-clamp-1"
              >
                {e.title || e.url}
              </a>
              <p className="text-gray-400 text-xs line-clamp-2">{e.snippet}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
