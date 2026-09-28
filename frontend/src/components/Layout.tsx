import { NavLink } from 'react-router-dom'
import {
  LayoutDashboard, Building2, ClipboardList, Map, Wrench,
  FileQuestion, FileText, Download, Settings, LogOut, Bell,
} from 'lucide-react'
import { logout } from '@/api/client'

const NAV_ITEMS = [
  { to: '/tableau-de-bord', label: 'Tableau de bord', icon: LayoutDashboard },
  { to: '/etablissements', label: 'Établissements', icon: Building2 },
  { to: '/visites', label: 'Visites', icon: ClipboardList },
  { to: '/cartographie', label: 'Cartographie', icon: Map },
  { to: '/equipements', label: 'Équipements', icon: Wrench },
  { to: '/questionnaires', label: 'Questionnaires', icon: FileQuestion },
  { to: '/rapports', label: 'Rapports', icon: FileText },
  { to: '/exports', label: 'Exports', icon: Download },
  { to: '/administration', label: 'Administration', icon: Settings },
]

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex min-h-screen bg-surface">
      <aside className="w-60 shrink-0 bg-secondary text-white/70 flex flex-col">
        <div className="px-5 py-5 flex items-center gap-2 text-white font-semibold text-lg border-b border-white/10">
          <span className="w-6 h-6 rounded-button bg-primary inline-block" />
          ARPENTEUR
        </div>
        <nav className="flex-1 py-3">
          {NAV_ITEMS.map(({ to, label, icon: Icon }) => (
            <NavLink
              key={to}
              to={to}
              className={({ isActive }) =>
                `flex items-center gap-3 px-5 py-2.5 text-sm transition-colors duration-200 ${
                  isActive
                    ? 'bg-primary text-white'
                    : 'hover:bg-white/5 hover:text-white'
                }`
              }
            >
              <Icon size={16} />
              {label}
            </NavLink>
          ))}
        </nav>
        <button
          onClick={() => {
            logout()
            window.location.href = '/connexion'
          }}
          className="flex items-center gap-3 px-5 py-3 text-sm border-t border-white/10 transition-colors duration-200 hover:bg-white/5 hover:text-white"
        >
          <LogOut size={16} />
          Déconnexion
        </button>
      </aside>

      <div className="flex-1 flex flex-col min-w-0">
        <header className="h-16 bg-surface-card border-b border-border flex items-center justify-end gap-4 px-6">
          <Bell size={18} className="text-muted" />
          <div className="w-8 h-8 rounded-full bg-border" />
        </header>
        <main className="flex-1 p-6 overflow-auto">{children}</main>
      </div>
    </div>
  )
}
