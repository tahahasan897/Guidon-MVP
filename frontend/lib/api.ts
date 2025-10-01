export async function api<T>(path: string, init?: RequestInit): Promise<T> {
  const base = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000'
  const res = await fetch(`${base}${path}`, {
    ...init,
    headers: {
      'Content-Type': 'application/json',
      ...(init?.headers || {}),
    },
    next: { revalidate: 0 },
  })
  if (!res.ok) throw new Error(`API error ${res.status}`)
  return res.json()
}
