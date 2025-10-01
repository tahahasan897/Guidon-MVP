"use client"
import { useEffect, useState } from 'react'
import { api } from '../lib/api'

type Metrics = { date: string; mrr: number; burn: number; runway_months: number; mom_growth: number }

export default function HomePage() {
  const [metrics, setMetrics] = useState<Metrics | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    ;(async () => {
      try {
        const data = await api<Metrics>("/api/metrics/latest")
        setMetrics(data)
      } catch {}
      setLoading(false)
    })()
  }, [])

  return (
    <main className="p-6">
      <h1 className="text-2xl font-semibold">founder-copilot</h1>
      <p className="text-gray-600 mt-2">Ingest, analyze, and act on your business data.</p>
      <div className="mt-6 grid grid-cols-1 gap-4 md:grid-cols-4">
        {loading ? (
          <div className="col-span-4 text-gray-600">Loading metrics...</div>
        ) : metrics ? (
          <>
            <Card title="MRR" value={`$${metrics.mrr.toFixed(0)}`} />
            <Card title="Burn" value={`$${metrics.burn.toFixed(0)}`} />
            <Card title="Runway" value={`${metrics.runway_months.toFixed(1)} mo`} />
            <Card title="MoM" value={`${(metrics.mom_growth * 100).toFixed(1)}%`} />
          </>
        ) : (
          <div className="col-span-4 text-gray-600">No metrics available yet.</div>
        )}
      </div>
    </main>
  )
}

function Card({ title, value }: { title: string; value: string }) {
  return (
    <div className="rounded-lg border bg-white p-4 shadow-sm">
      <div className="text-sm text-gray-600">{title}</div>
      <div className="mt-1 text-xl font-semibold">{value}</div>
    </div>
  )
}
