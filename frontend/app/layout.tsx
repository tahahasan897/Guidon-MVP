import './globals.css'
import type { Metadata } from 'next'
import Link from 'next/link'

export const metadata: Metadata = {
  title: 'founder-copilot',
  description: 'Ingest, analyze, and act on your business data',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-gray-50 text-gray-900">
        <nav className="flex gap-4 border-b bg-white p-4">
          <Link href="/">Dashboard</Link>
          <Link href="/connections">Connections</Link>
          <Link href="/runs">Runs</Link>
        </nav>
        {children}
      </body>
    </html>
  )
}
