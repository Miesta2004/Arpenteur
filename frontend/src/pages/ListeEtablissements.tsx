import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { api } from '@/api/client'
import type { Etablissement, PaginatedResponse } from '@/api/types'
import Layout from '@/components/Layout'
import { Search, Plus } from 'lucide-react'

export default function ListeEtablissements() {
  const [recherche, setRecherche] = useState('')

  const { data, isLoading } = useQuery({
    queryKey: ['etablissements', recherche],
    queryFn: async () =>
      (
        await api.get<PaginatedResponse<Etablissement>>('/etablissements/', {
          params: recherche ? { q: recherche } : {},
        })
      ).data,
  })

  return (
    <Layout>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-h2 font-semibold text-title">Établissements</h1>
        <button className="flex items-center gap-1.5 bg-primary hover:bg-primary-hover text-white text-sm font-medium px-3 py-2 rounded-button transition-colors duration-200">
          <Plus size={16} />
          Ajouter
        </button>
      </div>

      <div className="relative mb-4 max-w-sm">
        <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-muted" />
        <input
          value={recherche}
          onChange={(e) => setRecherche(e.target.value)}
          placeholder="Rechercher un établissement…"
          className="w-full pl-9 pr-3 py-2 text-sm rounded-button border border-border text-body focus:outline-none focus:ring-2 focus:ring-primary"
        />
      </div>

      <div className="bg-surface-card rounded-card border border-border overflow-hidden shadow-sm">
        <table className="w-full text-sm">
          <thead>
            <tr className="text-left text-xs text-muted bg-surface border-b border-border">
              <th className="px-4 py-2.5 font-medium">Nom</th>
              <th className="px-4 py-2.5 font-medium">Type</th>
              <th className="px-4 py-2.5 font-medium">Localisation</th>
              <th className="px-4 py-2.5 font-medium">Dernière visite</th>
            </tr>
          </thead>
          <tbody>
            {data?.results?.map((etab) => (
              <tr
                key={etab.id}
                className="border-b border-border last:border-0 hover:bg-surface cursor-pointer transition-colors duration-200"
              >
                <td className="px-4 py-2.5 text-title font-medium">{etab.nom}</td>
                <td className="px-4 py-2.5 text-muted">{etab.type}</td>
                <td className="px-4 py-2.5 text-muted">{etab.ville}</td>
                <td className="px-4 py-2.5 text-muted">{etab.derniere_visite_date ?? '—'}</td>
              </tr>
            ))}
            {!isLoading && !data?.results?.length && (
              <tr>
                <td colSpan={4} className="px-4 py-8 text-center text-muted">
                  Aucun établissement trouvé.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </Layout>
  )
}
