import '../globals.css'
import Link from 'next/link'

export default function NavLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
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
