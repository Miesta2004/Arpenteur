import { useQuery } from '@tanstack/react-query'
import { useNavigate } from 'react-router-dom'
import { api } from '@/api/client'
import type { TableauDeBord as TableauDeBordType } from '@/api/types'
import Layout from '@/components/Layout'
import { STATUT_LABELS, STATUT_STYLES } from '@/lib/statuts'
import { Building2, ClipboardList, Clock, FileText } from 'lucide-react'

const STAT_CARDS = [
    { key: 'nb_etablissements', label: 'Établissements', sous: 'Total recensés', icon: Building2 },
    { key: 'nb_visites', label: 'Visites', sous: 'Total visites', icon: ClipboardList },
    { key: 'nb_visites_en_cours', label: 'En cours', sous: 'Visites en cours', icon: Clock },
    { key: 'nb_rapports_generes', label: 'Rapports', sous: 'Rapports générés', icon: FileText },
] satisfies { key: Exclude<keyof TableauDeBordType, 'visites_recentes'>; label: string; sous: string; icon: typeof Building2 }[]

export default function TableauDeBord() {
    const navigate = useNavigate()
    const { data, isLoading } = useQuery({
        queryKey: ['tableau-de-bord'],
        queryFn: async () => (await api.get<TableauDeBordType>('/tableau-de-bord/')).data,
    })

    return (
        <Layout>
            <h1 className="text-h2 font-semibold text-title mb-1">Bonjour 👋</h1>
            <p className="text-body text-sm mb-6">Voici un aperçu de vos activités</p>

            <div className="grid grid-cols-4 gap-6 mb-6">
                {STAT_CARDS.map(({ key, label, sous, icon: Icon }) => (
                    <div key={key} className="bg-surface-card rounded-card border border-border p-6 shadow-sm">
                        <div className="flex items-center justify-between mb-2">
                            <span className="text-xs font-medium text-muted">{label}</span>
                            <Icon size={16} className="text-accent" />
                        </div>
                        <div className="text-2xl font-semibold text-title">
                            {isLoading ? '—' : (data?.[key] ?? 0)}
                        </div>
                        <div className="text-xs text-muted mt-1">{sous}</div>
                    </div>
                ))}
            </div>

            <div className="bg-surface-card rounded-card border border-border p-6 shadow-sm">
                <h2 className="text-sm font-semibold text-title mb-3">Visites récentes</h2>
                <table className="w-full text-sm">
                    <thead>
                    <tr className="text-left text-xs text-muted border-b border-border">
                        <th className="pb-2 font-medium">Établissement</th>
                        <th className="pb-2 font-medium">Date</th>
                        <th className="pb-2 font-medium">Statut</th>
                        <th className="pb-2 font-medium">Progression</th>
                    </tr>
                    </thead>
                    <tbody>
                    {data?.visites_recentes?.map((v) => (
                        <tr
                            key={v.id}
                            onClick={() => navigate(`/visites/${v.id}`)}
                            className="border-b border-border last:border-0 hover:bg-surface cursor-pointer transition-colors duration-200"
                        >
                            <td className="py-2 text-body">{v.etablissement_nom}</td>
                            <td className="py-2 text-muted">{v.date_visite}</td>
                            <td className="py-2">
                  <span className={`px-2 py-0.5 rounded-full text-xs ${STATUT_STYLES[v.statut]}`}>
                    {STATUT_LABELS[v.statut]}
                  </span>
                            </td>
                            <td className="py-2 text-muted">{v.avancement}%</td>
                        </tr>
                    ))}
                    {!isLoading && !data?.visites_recentes?.length && (
                        <tr>
                            <td colSpan={4} className="py-6 text-center text-muted">
                                Aucune visite pour l'instant.
                            </td>
                        </tr>
                    )}
                    </tbody>
                </table>
            </div>
        </Layout>
    )
}