import { useState } from 'react'
import { useParams } from 'react-router-dom'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { api } from '@/api/client'
import type { Commentaire, Visite } from '@/api/types'
import Layout from '@/components/Layout'
import { STATUT_LABELS, STATUT_STYLES } from '@/lib/statuts'
import { Send } from 'lucide-react'

const ONGLETS = ['Aperçu', 'Questionnaires', 'Bâtiments', 'Cartographie', 'Photos', 'Rapport'] as const

// Sections de progression affichées — dérivées des mêmes booléens que Visite.avancement
// côté backend (Partie 3). Volontairement en tout-ou-rien (0% / 100%) : le modèle actuel
// ne calcule pas de progression fine par section, seulement "rempli / pas rempli".
function calculerSections(v: Visite) {
    return [
        { label: 'Informations générales', fait: !!v.etat_locaux },
        { label: 'Cartographie (bâtiments/services)', fait: (v.nb_batiments ?? 0) > 0 || (v.nb_zones ?? 0) > 0 },
        { label: 'Chambres et lits', fait: (v.nb_chambres ?? 0) > 0 || (v.nb_lits ?? 0) > 0 },
        { label: 'Audit IT', fait: !!v.reseau_disponible || !!v.wifi_disponible || !!v.observations_it },
        {
            label: 'Effectifs',
            fait: !!(v.effectif_medecins || v.effectif_infirmiers || v.effectif_autres),
        },
        { label: 'Processus et priorités', fait: !!v.processus_actuels || !!v.priorites_contraintes },
    ]
}

export default function DetailVisite() {
    const { id } = useParams()
    const [ongletActif, setOngletActif] = useState(0)
    const [texteCommentaire, setTexteCommentaire] = useState('')
    const queryClient = useQueryClient()

    const { data: visite, isLoading } = useQuery({
        queryKey: ['visite', id],
        queryFn: async () => (await api.get<Visite>(`/visites/${id}/`)).data,
    })

    const ajouterCommentaire = useMutation({
        mutationFn: async (texte: string) =>
            (await api.post<Commentaire>('/commentaires/', { visite: id, texte })).data,
        onSuccess: () => {
            setTexteCommentaire('')
            queryClient.invalidateQueries({ queryKey: ['visite', id] })
        },
    })

    if (isLoading) {
        return (
            <Layout>
                <p className="text-muted">Chargement…</p>
            </Layout>
        )
    }

    if (!visite) {
        return (
            <Layout>
                <p className="text-muted">Visite introuvable.</p>
            </Layout>
        )
    }

    const inspecteurPrincipal = visite.membres_equipe?.find((m) => m.est_inspecteur_principal)
    const nomInspecteur = inspecteurPrincipal
        ? `${inspecteurPrincipal.utilisateur.first_name} ${inspecteurPrincipal.utilisateur.last_name}`.trim() ||
        inspecteurPrincipal.utilisateur.username
        : visite.auteur || '—'
    const tailleEquipe = visite.membres_equipe?.length ?? 0

    return (
        <Layout>
            <div className="flex items-center justify-between mb-1">
                <div className="flex items-center gap-3">
                    <h1 className="text-h2 font-semibold text-title">
                        Visite — {visite.etablissement_nom ?? `Établissement #${visite.etablissement}`}
                    </h1>
                    <span className={`px-2 py-0.5 rounded-full text-xs ${STATUT_STYLES[visite.statut]}`}>
            {STATUT_LABELS[visite.statut]}
          </span>
                </div>
            </div>

            {/* Barre d'infos */}
            <div className="grid grid-cols-4 gap-6 mt-4 mb-6">
                <InfoRapide label="Date de début" valeur={visite.date_visite} />
                <InfoRapide label="Inspecteur" valeur={nomInspecteur} />
                <InfoRapide label="Équipe" valeur={`${tailleEquipe} personne${tailleEquipe > 1 ? 's' : ''}`} />
                <InfoRapide label="Progression globale" valeur={`${visite.avancement}%`} />
            </div>

            {/* Onglets — seul "Aperçu" a un contenu construit pour l'instant */}
            <div className="flex gap-1 border-b border-border mb-6">
                {ONGLETS.map((onglet, i) => (
                    <button
                        key={onglet}
                        disabled={i !== 0}
                        onClick={() => setOngletActif(i)}
                        className={`px-3 py-2 text-sm border-b-2 transition-colors duration-200 ${
                            i === ongletActif
                                ? 'border-primary text-primary font-medium'
                                : 'border-transparent text-muted cursor-not-allowed opacity-50'
                        }`}
                        title={i !== 0 ? 'Écran à venir' : undefined}
                    >
                        {onglet}
                    </button>
                ))}
            </div>

            <div className="grid grid-cols-2 gap-6">
                {/* --- Progression par section --- */}
                <div className="bg-surface-card rounded-card border border-border p-6 shadow-sm h-fit">
                    <h2 className="text-sm font-semibold text-title mb-4">Progression par section</h2>
                    <div className="space-y-3">
                        {calculerSections(visite).map(({ label, fait }) => (
                            <div key={label}>
                                <div className="flex items-center justify-between text-sm mb-1">
                                    <span className="text-body">{label}</span>
                                    <span className="text-muted text-xs">{fait ? '100%' : '0%'}</span>
                                </div>
                                <div className="h-1.5 rounded-full bg-border overflow-hidden">
                                    <div
                                        className={`h-full rounded-full transition-all duration-300 ${fait ? 'bg-success' : 'bg-border'}`}
                                        style={{ width: fait ? '100%' : '0%' }}
                                    />
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

                {/* --- Commentaires récents --- */}
                <div className="bg-surface-card rounded-card border border-border p-6 shadow-sm h-fit">
                    <h2 className="text-sm font-semibold text-title mb-4">Commentaires récents</h2>

                    <form
                        onSubmit={(e) => {
                            e.preventDefault()
                            if (texteCommentaire.trim()) ajouterCommentaire.mutate(texteCommentaire.trim())
                        }}
                        className="flex gap-2 mb-4"
                    >
                        <input
                            value={texteCommentaire}
                            onChange={(e) => setTexteCommentaire(e.target.value)}
                            placeholder="Ajouter un commentaire…"
                            className="flex-1 rounded-button border border-border px-3 py-2 text-sm text-body focus:outline-none focus:ring-2 focus:ring-primary"
                        />
                        <button
                            type="submit"
                            disabled={ajouterCommentaire.isPending || !texteCommentaire.trim()}
                            className="flex items-center justify-center w-9 h-9 rounded-button bg-primary hover:bg-primary-hover disabled:opacity-50 text-white transition-colors duration-200 shrink-0"
                        >
                            <Send size={15} />
                        </button>
                    </form>

                    <div className="space-y-4">
                        {visite.commentaires?.map((c) => (
                            <div key={c.id} className="flex gap-3 text-sm">
                                <div className="w-7 h-7 rounded-full bg-accent/10 text-accent flex items-center justify-center text-xs font-medium shrink-0">
                                    {(c.auteur?.first_name?.[0] ?? c.auteur?.username?.[0] ?? '?').toUpperCase()}
                                </div>
                                <div>
                                    <div className="text-muted text-xs mb-0.5">
                                        {new Date(c.date_creation).toLocaleString('fr-FR', {
                                            day: '2-digit',
                                            month: 'short',
                                            hour: '2-digit',
                                            minute: '2-digit',
                                        })}
                                    </div>
                                    <p className="text-body">{c.texte}</p>
                                </div>
                            </div>
                        ))}
                        {!visite.commentaires?.length && (
                            <p className="text-sm text-muted">Aucun commentaire pour l'instant.</p>
                        )}
                    </div>
                </div>
            </div>
        </Layout>
    )
}

function InfoRapide({ label, valeur }: { label: string; valeur: string }) {
    return (
        <div className="bg-surface-card rounded-card border border-border p-4 shadow-sm">
            <div className="text-xs text-muted mb-1">{label}</div>
            <div className="text-sm font-semibold text-title">{valeur}</div>
        </div>
    )
}