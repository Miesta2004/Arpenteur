import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { login } from '@/api/client'

export default function EcranConnexion() {
  const navigate = useNavigate()
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [erreur, setErreur] = useState<string | null>(null)
  const [enCours, setEnCours] = useState(false)

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    setErreur(null)
    setEnCours(true)
    try {
      await login(username, password)
      navigate('/tableau-de-bord')
    } catch {
      setErreur("Nom d'utilisateur ou mot de passe incorrect.")
    } finally {
      setEnCours(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-surface px-4">
      <div className="w-full max-w-sm">
        <div className="flex items-center gap-2 justify-center mb-1 text-secondary font-bold text-2xl">
          <span className="w-7 h-7 rounded-button bg-primary inline-block" />
          ARPENTEUR
        </div>
        <p className="text-center text-muted text-sm mb-8">
          Recenser. Cartographier. Comprendre.
        </p>

        <form
          onSubmit={handleSubmit}
          className="bg-surface-card border border-border rounded-card p-6 shadow-sm"
        >
          <label className="block text-sm font-medium text-title mb-1">
            Nom d'utilisateur
          </label>
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
            className="w-full mb-4 rounded-button border border-border px-3 py-2 text-sm text-body focus:outline-none focus:ring-2 focus:ring-primary"
          />

          <label className="block text-sm font-medium text-title mb-1">
            Mot de passe
          </label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            className="w-full mb-2 rounded-button border border-border px-3 py-2 text-sm text-body focus:outline-none focus:ring-2 focus:ring-primary"
          />

          {erreur && <p className="text-sm text-danger mb-2">{erreur}</p>}

          <button
            type="submit"
            disabled={enCours}
            className="w-full mt-3 bg-primary hover:bg-primary-hover disabled:opacity-60 text-white text-sm font-medium py-2.5 rounded-button transition-colors duration-200"
          >
            {enCours ? 'Connexion…' : 'Se connecter'}
          </button>
        </form>

        <p className="text-center text-xs text-muted mt-6">
          © {new Date().getFullYear()} Arpenteur. Tous droits réservés.
        </p>
      </div>
    </div>
  )
}
