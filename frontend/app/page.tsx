import Navbar from "@/components/landing/Navbar"
import Link from "next/link"

export default function HomePage() {
  return(
    <div className="min-h-screen bg-slate-950 text-white">
      <Navbar />
      <main className="mx-auto max-w-5xl px-6 py-28">
        <p className="text-sm font-semibold uppercase tracking-[0.2em] text-cyan-300">Research, with a trail</p>
        <h1 className="mt-5 max-w-3xl text-5xl font-semibold tracking-tight sm:text-7xl">Turn a question into a body of evidence.</h1>
        <p className="mt-7 max-w-xl text-lg leading-8 text-slate-300">Create a private research project, discover academic papers, and keep the sources that move your thinking forward.</p>
        <Link href="/dashboard" className="mt-9 inline-block rounded-lg bg-cyan-400 px-5 py-3 text-sm font-semibold text-slate-950 hover:bg-cyan-300">Open workspace</Link>
      </main>
    </div>
  )
}