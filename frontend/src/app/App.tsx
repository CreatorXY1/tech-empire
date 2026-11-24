import { useEffect, useState } from 'react'
import { Activity, ArrowUpRight, Cpu, Factory, FlaskConical, Gauge, Layers3, Radio, Wrench } from 'lucide-react'
import { getBackendHealth, type ConnectionState } from '../services/health'

const navigation = [
  { label: 'Overview', icon: Gauge, active: true },
  { label: 'Workshop', icon: Wrench, active: false },
  { label: 'Manufacturing', icon: Factory, active: false },
  { label: 'Technology', icon: FlaskConical, active: false },
]

const HEALTH_CHECK_INTERVAL_MS = 30_000
const HEALTH_CHECK_TIMEOUT_MS = 5_000

function statusLabel(state: ConnectionState) {
  if (state === 'connected') return 'Connected'
  if (state === 'disconnected') return 'Disconnected'
  return 'Checking connection'
}

export default function App() {
  const [connection, setConnection] = useState<ConnectionState>('checking')

  useEffect(() => {
    let isMounted = true
    let activeController: AbortController | undefined

    const checkBackend = async () => {
      const controller = new AbortController()
      activeController = controller
      const timeoutId = window.setTimeout(() => controller.abort(), HEALTH_CHECK_TIMEOUT_MS)

      try {
        await getBackendHealth(controller.signal)
        if (isMounted) setConnection('connected')
      } catch {
        if (isMounted) setConnection('disconnected')
      } finally {
        window.clearTimeout(timeoutId)
        if (activeController === controller) activeController = undefined
      }
    }

    void checkBackend()
    const intervalId = window.setInterval(() => void checkBackend(), HEALTH_CHECK_INTERVAL_MS)

    return () => {
      isMounted = false
      window.clearInterval(intervalId)
      activeController?.abort()
    }
  }, [])

  return (
    <div className="min-h-screen bg-[#080f1b] text-slate-100">
      <div className="mx-auto flex min-h-screen max-w-[1600px]">
        <aside className="hidden w-64 shrink-0 border-r border-white/[0.07] bg-[#0b1422] px-5 py-7 lg:flex lg:flex-col">
          <div className="flex items-center gap-3 px-2">
            <div className="grid size-10 place-items-center rounded-xl bg-cyan-400/10 text-cyan-300 ring-1 ring-cyan-300/20"><Cpu size={21} /></div>
            <div><p className="text-sm font-semibold tracking-wide">TECH EMPIRE</p><p className="mt-0.5 text-[10px] uppercase tracking-[0.2em] text-slate-500">Industrial systems</p></div>
          </div>
          <div className="mt-12 px-3 text-[10px] font-semibold uppercase tracking-[0.2em] text-slate-600">Operations</div>
          <nav className="mt-3 space-y-1" aria-label="Main navigation">
            {navigation.map(({ label, icon: Icon, active }) => (
              <div key={label} aria-current={active ? 'page' : undefined} className={`flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm ${active ? 'bg-cyan-300/[0.09] text-cyan-200 ring-1 ring-cyan-300/10' : 'text-slate-400'}`}>
                <Icon size={17} strokeWidth={1.8} /><span>{label}</span>{!active && <span className="ml-auto text-[9px] uppercase tracking-wider text-slate-600">Soon</span>}
              </div>
            ))}
          </nav>
          <div className="mt-auto rounded-xl border border-white/[0.07] bg-white/[0.025] p-4">
            <div className="flex items-center gap-2 text-xs font-medium text-slate-300"><Radio size={14} className="text-cyan-300" /> Local development</div>
            <p className="mt-2 text-[11px] leading-relaxed text-slate-500">Your workshop foundation is being assembled.</p>
          </div>
        </aside>

        <main className="min-w-0 flex-1 px-5 py-6 sm:px-8 sm:py-9 lg:px-12">
          <header className="flex flex-wrap items-center justify-between gap-4 border-b border-white/[0.07] pb-6">
            <div><p className="text-[11px] uppercase tracking-[0.2em] text-cyan-300/70">Command center / setup</p><h1 className="mt-2 text-2xl font-semibold tracking-tight sm:text-3xl">Welcome to Tech Empire</h1></div>
            <div className="flex items-center gap-2 rounded-full border border-white/[0.08] bg-white/[0.03] px-3.5 py-2 text-xs text-slate-300" role="status" aria-live="polite">
              <span className={`size-2 rounded-full ${connection === 'connected' ? 'bg-emerald-400' : connection === 'disconnected' ? 'bg-rose-400' : 'animate-pulse bg-amber-300'}`} />
              Backend: {statusLabel(connection)}
            </div>
          </header>

          <section className="relative mt-8 overflow-hidden rounded-2xl border border-cyan-200/10 bg-gradient-to-br from-[#10243a] via-[#0c1b2d] to-[#0b1422] p-6 sm:p-9">
            <div className="absolute -right-10 -top-24 size-72 rounded-full border border-cyan-300/[0.07]" /><div className="absolute -right-2 -top-16 size-56 rounded-full border border-cyan-300/[0.07]" />
            <div className="relative max-w-2xl">
              <div className="inline-flex items-center gap-2 rounded-full border border-cyan-300/15 bg-cyan-300/[0.06] px-3 py-1.5 text-[10px] font-medium uppercase tracking-[0.16em] text-cyan-200"><Activity size={13} /> Foundation phase</div>
              <h2 className="mt-5 text-2xl font-semibold leading-tight sm:text-4xl">Build the capabilities<br className="hidden sm:block" /> behind every product.</h2>
              <p className="mt-4 max-w-xl text-sm leading-6 text-slate-400">Your industrial journey starts with a workshop. This development shell is ready for the first playable systems to take shape.</p>
              <div className="mt-7 inline-flex items-center gap-2 text-xs font-medium text-cyan-200/80">Game systems arrive in later phases <ArrowUpRight size={14} /></div>
            </div>
          </section>

          <section className="mt-8" aria-labelledby="systems-heading">
            <div className="flex items-end justify-between"><div><p className="text-[10px] uppercase tracking-[0.2em] text-slate-500">Development roadmap</p><h2 id="systems-heading" className="mt-2 text-lg font-semibold">Core systems</h2></div><span className="text-xs text-slate-500">Phase 1 · Application shell</span></div>
            <div className="mt-4 grid gap-3 sm:grid-cols-2 xl:grid-cols-3">
              {[
                { title: 'Workshop', detail: 'Facilities and equipment', icon: Wrench },
                { title: 'Manufacturing', detail: 'Processes and production', icon: Factory },
                { title: 'Technology', detail: 'Research and capability', icon: Layers3 },
              ].map(({ title, detail, icon: Icon }) => <article key={title} className="rounded-xl border border-white/[0.07] bg-[#0c1624] p-5"><div className="flex size-9 items-center justify-center rounded-lg bg-white/[0.04] text-slate-400"><Icon size={17} /></div><h3 className="mt-4 text-sm font-medium">{title}</h3><p className="mt-1 text-xs text-slate-500">{detail} <span className="text-slate-600">· Coming in a later phase</span></p></article>)}
            </div>
          </section>
          <footer className="mt-10 border-t border-white/[0.06] pt-5 text-[11px] text-slate-600">Local-first development · No game save has been created</footer>
        </main>
      </div>
    </div>
  )
}
