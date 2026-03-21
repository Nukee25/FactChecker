import React, { useState } from 'react'
import Header from './components/Header'
import InputForm from './components/InputForm'
import ProgressTracker from './components/ProgressTracker'
import AccuracyReport from './components/AccuracyReport'

export default function App() {
  const [input, setInput] = useState('')
  const [inputType, setInputType] = useState('text')
  const [isLoading, setIsLoading] = useState(false)
  const [stage, setStage] = useState('')
  const [progress, setProgress] = useState(0)
  const [progressMessage, setProgressMessage] = useState('')
  const [report, setReport] = useState(null)
  const [currentClaim, setCurrentClaim] = useState(0)
  const [totalClaims, setTotalClaims] = useState(0)
  const [error, setError] = useState(null)

  const handleVerify = async () => {
    setIsLoading(true)
    setReport(null)
    setError(null)
    setStage('extracting')
    setProgress(0)
    setProgressMessage('Starting verification...')
    setCurrentClaim(0)
    setTotalClaims(0)

    try {
      const response = await fetch('/api/verify', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ input, input_type: inputType }),
      })

      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`)
      }

      const reader = response.body.getReader()
      const decoder = new TextDecoder()
      let buffer = ''

      while (true) {
        const { done, value } = await reader.read()
        if (done) break

        buffer += decoder.decode(value, { stream: true })
        const lines = buffer.split('\n')
        buffer = lines.pop()

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const event = JSON.parse(line.slice(6))
              setStage(event.stage)
              setProgress(event.progress ?? 0)
              setProgressMessage(event.message ?? '')

              if (event.stage === 'verifying') {
                setCurrentClaim(event.current_claim ?? 0)
                setTotalClaims(event.total_claims ?? 0)
              }

              if (event.stage === 'complete') {
                setReport(event.report)
                setIsLoading(false)
              }

              if (event.stage === 'error') {
                setError(event.message)
                setIsLoading(false)
              }
            } catch {
              // ignore malformed SSE lines
            }
          }
        }
      }
    } catch (err) {
      setError(err.message)
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-950 text-white">
      <Header />
      <main className="max-w-4xl mx-auto px-4 py-8 space-y-6">
        <InputForm
          input={input}
          setInput={setInput}
          inputType={inputType}
          setInputType={setInputType}
          onVerify={handleVerify}
          isLoading={isLoading}
        />

        {error && (
          <div className="bg-red-900/40 border border-red-500 rounded-xl p-4 text-red-300">
            <span className="font-semibold">Error: </span>{error}
          </div>
        )}

        {isLoading && (
          <ProgressTracker
            stage={stage}
            progress={progress}
            message={progressMessage}
            currentClaim={currentClaim}
            totalClaims={totalClaims}
          />
        )}

        {report && <AccuracyReport report={report} />}
      </main>
    </div>
  )
}
