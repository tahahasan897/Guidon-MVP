"use client"
import { useEffect, useState } from 'react'
import { api } from '../../lib/api'

type Run = { id: number; status: string; goal?: string }

type Action = { id: number; run_id: number; status: string }

export default function RunsPage() {
  const [runs, setRuns] = useState<Run[]>([])
  const [actions, setActions] = useState<Action[]>([])
  const [goal, setGoal] = useState('Prepare weekly growth summary')

  async function load() {
    const rs = await api<Run[]>("/api/runs/")
    setRuns(rs)
    if (rs.length) {
      const acts = await api<Action[]>(`/api/actions/by_run/${rs[0].id}`)
      setActions(acts)
    }
  }

  async function trigger() {
    await api("/api/agent/run", { method: 'POST', body: JSON.stringify({ goal, mode: 'on_demand' }) })
    load()
  }

  async function approve(actionId: number) {
    await api("/api/agent/confirm_action", { method: 'POST', body: JSON.stringify({ action_id: actionId }) })
    load()
  }

  useEffect(() => { load() }, [])

  return (
    <main className="p-6">
      <h1 className="text-2xl font-semibold">Agent Runs</h1>
      <div className="mt-4 flex gap-2">
        <input className="rounded border px-3 py-2" value={goal} onChange={e => setGoal(e.target.value)} />
        <button className="rounded bg-blue-600 px-3 py-2 text-white" onClick={trigger}>Run</button>
      </div>
      <div className="mt-6 grid grid-cols-1 gap-4 md:grid-cols-2">
        <div className="rounded border bg-white p-4">
          <h2 className="font-medium">Runs</h2>
          <ul className="mt-2 space-y-2">
            {runs.map(r => <li key={r.id} className="rounded border p-2">#{r.id} – {r.status} – {r.goal || ''}</li>)}
          </ul>
        </div>
        <div className="rounded border bg-white p-4">
          <h2 className="font-medium">Actions</h2>
          <ul className="mt-2 space-y-2">
            {actions.map(a => (
              <li key={a.id} className="flex items-center justify-between rounded border p-2">
                <span>#{a.id} – {a.status}</span>
                {a.status === 'pending' && (
                  <button className="rounded bg-green-600 px-2 py-1 text-white" onClick={() => approve(a.id)}>Approve</button>
                )}
              </li>
            ))}
          </ul>
        </div>
      </div>
    </main>
  )
}
