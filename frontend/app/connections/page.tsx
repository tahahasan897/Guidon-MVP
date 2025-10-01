"use client"
import { useEffect, useState } from 'react'
import { api } from '../../lib/api'

type Conn = { id: number; provider: string; status: string }

export default function ConnectionsPage() {
  const [items, setItems] = useState<Conn[]>([])
  const [loading, setLoading] = useState(true)

  async function load() {
    setLoading(true)
    const data = await api<Conn[]>("/api/connections/")
    setItems(data)
    setLoading(false)
  }

  useEffect(() => { load() }, [])

  async function add(provider: string) {
    await api<Conn>("/api/connections/", { method: 'POST', body: JSON.stringify({ provider }) })
    load()
  }

  async function remove(id: number) {
    await api("/api/connections/" + id, { method: 'DELETE' })
    load()
  }

  return (
    <main className="p-6">
      <h1 className="text-2xl font-semibold">Connections</h1>
      <div className="mt-4 flex gap-2">
        <button className="rounded bg-blue-600 px-3 py-2 text-white" onClick={() => add('google')}>Connect Google</button>
        <button className="rounded bg-black px-3 py-2 text-white" onClick={() => add('notion')}>Connect Notion</button>
      </div>
      <div className="mt-6">
        {loading ? <p>Loading...</p> : (
          <ul className="space-y-2">
            {items.map(i => (
              <li key={i.id} className="flex items-center justify-between rounded border bg-white p-3">
                <span>{i.provider} – {i.status}</span>
                <button onClick={() => remove(i.id)} className="text-red-600">Delete</button>
              </li>
            ))}
          </ul>
        )}
      </div>
    </main>
  )
}
