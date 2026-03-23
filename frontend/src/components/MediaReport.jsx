import React from 'react'

function probabilityColor(prob) {
  if (prob <= 30) return 'text-green-400'
  if (prob <= 60) return 'text-yellow-400'
  return 'text-red-400'
}

function probabilityBarColor(prob) {
  if (prob <= 30) return 'bg-green-500'
  if (prob <= 60) return 'bg-yellow-500'
  return 'bg-red-500'
}

export default function MediaReport({ result }) {
  const manipProb = result.manipulation_probability ?? 0
  const aiProb = result.ai_generated_probability ?? 0
  const confidence = result.confidence ?? 0
  const isAuthentic = result.is_authentic

  const authenticityLabel =
    isAuthentic === true ? '✅ Likely Authentic' :
    isAuthentic === false ? '❌ Likely Manipulated / AI-Generated' :
    '❓ Inconclusive'

  const authenticityColor =
    isAuthentic === true ? 'text-green-400' :
    isAuthentic === false ? 'text-red-400' :
    'text-gray-400'

  return (
    <div className="bg-gray-900 border border-gray-700 rounded-2xl p-6 shadow-xl space-y-5">
      <h2 className="text-lg font-bold text-white">🖼️ Media Authenticity Report</h2>

      {/* Overall verdict */}
      <div className="flex items-center justify-between bg-gray-800 rounded-xl px-5 py-4">
        <span className="text-gray-400 text-sm font-medium">Verdict</span>
        <span className={`text-base font-bold ${authenticityColor}`}>{authenticityLabel}</span>
      </div>

      {/* Confidence */}
      <div>
        <div className="flex justify-between text-sm text-gray-400 mb-1">
          <span>Analysis Confidence</span>
          <span className="text-white font-medium">{confidence}%</span>
        </div>
        <div className="w-full bg-gray-800 rounded-full h-2">
          <div
            className="bg-blue-500 h-2 rounded-full transition-all duration-700"
            style={{ width: `${confidence}%` }}
          />
        </div>
      </div>

      {/* Manipulation probability */}
      <div>
        <div className="flex justify-between text-sm text-gray-400 mb-1">
          <span>Manipulation Probability</span>
          <span className={`font-medium ${probabilityColor(manipProb)}`}>{manipProb}%</span>
        </div>
        <div className="w-full bg-gray-800 rounded-full h-2">
          <div
            className={`${probabilityBarColor(manipProb)} h-2 rounded-full transition-all duration-700`}
            style={{ width: `${manipProb}%` }}
          />
        </div>
      </div>

      {/* AI-generated probability */}
      <div>
        <div className="flex justify-between text-sm text-gray-400 mb-1">
          <span>AI-Generated Probability</span>
          <span className={`font-medium ${probabilityColor(aiProb)}`}>{aiProb}%</span>
        </div>
        <div className="w-full bg-gray-800 rounded-full h-2">
          <div
            className={`${probabilityBarColor(aiProb)} h-2 rounded-full transition-all duration-700`}
            style={{ width: `${aiProb}%` }}
          />
        </div>
      </div>

      {/* Summary */}
      {result.summary && (
        <div className="bg-gray-800 rounded-xl p-4">
          <p className="text-xs text-gray-500 uppercase tracking-wide mb-2">Summary</p>
          <p className="text-gray-300 text-sm leading-relaxed">{result.summary}</p>
        </div>
      )}

      {/* Indicators */}
      {(result.indicators || []).length > 0 && (
        <div>
          <p className="text-xs text-gray-500 uppercase tracking-wide mb-2">Indicators</p>
          <ul className="space-y-1">
            {result.indicators.map((ind, i) => (
              <li key={i} className="text-gray-300 text-sm flex items-start gap-2">
                <span className="text-gray-600 mt-0.5">•</span>
                {ind}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}
