import { useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import { api } from '@/api/client'
import type { Etablissement, PaginatedResponse, Visite } from '@/api/types'
import Layout from '@/components/Layout'
import ResumeCartographie from '@/components/ResumeCartographie'
import ArborescenceCartographie, { STATUT_ZONE_LABELS, STATUT_ZONE_STYLES } from '@/components/ArborescenceCartographie'
import { STATUT_ETABLISSEMENT_LABELS, STATUT_ETABLISSEMENT_STYLES, STATUT_LABELS, STATUT_STYLES } from '@/lib/statuts'
import { Plus, MapPin } from 'lucide-react'

// Icône de marqueur en SVG inline (pas d'image externe à charger/configurer avec Vite)
const MARQUEUR = L.divIcon({
    className: '',
    html: `<div style="width:16px;height:16px;border-radius:50%;background:#0F766E;border:3px solid white;box-shadow:0 1px 4px rgba(0,0,0,0.4)"></div>`,
    iconSize: [16, 16],
    iconAnchor: [8, 8],
})

// Onglets actifs (index) → onglets pas encore construits (le reste, désactivés)
const ONGLETS = ['Informations', 'Visites', 'Bâtiments', 'Équipements', 'Documents', 'Photos'] as const
const DERNIER_ONGLET_ACTIF = 2 // "Bâtiments" — au-delà, écrans à venir

export default function DetailEtablissement() {
    const { id } = useParams()
    const navigate = useNavigate()
    const [ongletActif, setOngletActif] = useState(0)

    const { data: etab, isLoading } = useQuery({
        queryKey: ['etablissement', id],
        queryFn: async () => (await api.get<Etablissement>(`/etablissements/${id}/`)).data,
    })

    // enabled: false tant que l'onglet Visites n'est pas ouvert — pas la peine de
    // charger ces données si l'utilisateur reste sur "Informations".
    const { data: visites, isLoading: visitesLoading } = useQuery({
        queryKey: ['visites', 'etablissement', id],
        queryFn: async () =>
            (await api.get<PaginatedResponse<Visite>>('/visites/', { params: { etablissement: id } })).data,
        enabled: ongletActif === 1,
    })

    if (isLoading) {
        return (
            <Layout>
                <p className="text-muted">Chargement…</p>
            </Layout>
        )
    }

    if (!etab) {
        return (
            <Layout>
                <p className="text-muted">Établissement introuvable.</p>
            </Layout>
        )
    }

    const lat = etab.latitude ? parseFloat(etab.latitude) : null
    const lng = etab.longitude ? parseFloat(etab.longitude) : null

    return (
        <Layout>
            <div className="flex items-center justify-between mb-1">
                <div className="flex items-center gap-3">
                    <h1 className="text-h2 font-semibold text-title">{etab.nom}</h1>
                    <span className={`px-2 py-0.5 rounded-full text-xs ${STATUT_ETABLISSEMENT_STYLES[etab.statut]}`}>
            {STATUT_ETABLISSEMENT_LABELS[etab.statut]}
          </span>
                </div>
                <button
                    onClick={() => navigate(`/visites/nouvelle?etablissement=${etab.id}`)}
                    className="flex items-center gap-1.5 bg-primary hover:bg-primary-hover text-white text-sm font-medium px-3 py-2 rounded-button transition-colors duration-200"
                >
                    <Plus size={16} />
                    Nouvelle visite
                </button>
            </div>

            {/* Onglets — "Informations" et "Visites" ont un contenu construit, le reste à venir */}
            <div className="flex gap-1 border-b border-border mb-6 mt-4">
                {ONGLETS.map((onglet, i) => (
                    <button
                        key={onglet}
                        disabled={i > DERNIER_ONGLET_ACTIF}
                        onClick={() => setOngletActif(i)}
                        className={`px-3 py-2 text-sm border-b-2 transition-colors duration-200 ${
                            i === ongletActif
                                ? 'border-primary text-primary font-medium'
                                : i > DERNIER_ONGLET_ACTIF
                                    ? 'border-transparent text-muted cursor-not-allowed opacity-50'
                                    : 'border-transparent text-muted hover:text-title'
                        }`}
                        title={i > DERNIER_ONGLET_ACTIF ? 'Écran à venir' : undefined}
                    >
                        {onglet}
                    </button>
                ))}
            </div>

            {ongletActif === 0 && (
                <div className="grid grid-cols-3 gap-6">
                    {/* --- Colonne gauche : infos générales --- */}
                    <div className="col-span-2 space-y-6">
                        <div className="bg-surface-card rounded-card border border-border p-6 shadow-sm">
                            <h2 className="text-sm font-semibold text-title mb-4">Informations générales</h2>
                            <dl className="grid grid-cols-2 gap-y-3 text-sm">
                                <Champ label="Type" valeur={etab.type} />
                                <Champ label="Adresse" valeur={etab.adresse || '—'} />
                                <Champ label="Région" valeur={etab.region || '—'} />
                                <Champ label="Téléphone" valeur={etab.contact_telephone || '—'} />
                                <Champ label="Email" valeur={etab.contact_email || '—'} />
                                <Champ label="Capacité (lits)" valeur={String(etab.nb_lits ?? 0)} />
                            </dl>
                        </div>

                        <div className="bg-surface-card rounded-card border border-border p-6 shadow-sm">
                            <h2 className="text-sm font-semibold text-title mb-4 flex items-center gap-1.5">
                                <MapPin size={15} className="text-accent" />
                                Localisation
                            </h2>
                            {lat != null && lng != null ? (
                                <div className="rounded-button overflow-hidden border border-border h-64">
                                    <MapContainer center={[lat, lng]} zoom={15} className="w-full h-full">
                                        <TileLayer
                                            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                                            attribution="&copy; OpenStreetMap"
                                        />
                                        <Marker position={[lat, lng]} icon={MARQUEUR}>
                                            <Popup>{etab.nom}</Popup>
                                        </Marker>
                                    </MapContainer>
                                </div>
                            ) : (
                                <p className="text-sm text-muted">Coordonnées GPS non renseignées.</p>
                            )}
                        </div>
                    </div>

                    {/* --- Colonne droite : résumé --- */}
                    <ResumeCartographie etablissement={etab} />
                </div>
            )}

            {ongletActif === 2 && (
                <div className="grid grid-cols-3 gap-6">
                    <div className="col-span-2">
                        <ArborescenceCartographie etablissement={etab} />
                    </div>
                    <div className="space-y-6">
                        <ResumeCartographie etablissement={etab} />
                        <div className="bg-surface-card rounded-card border border-border p-6 shadow-sm">
                            <h2 className="text-sm font-semibold text-title mb-3">Légende</h2>
                            <div className="space-y-2">
                                {(Object.keys(STATUT_ZONE_LABELS) as (keyof typeof STATUT_ZONE_LABELS)[]).map((statut) => (
                                    <div key={statut} className="flex items-center gap-2 text-sm text-body">
                                        <span className={`w-2 h-2 rounded-full ${STATUT_ZONE_STYLES[statut]}`} />
                                        {STATUT_ZONE_LABELS[statut]}
                                    </div>
                                ))}
                            </div>
                        </div>
                    </div>
                </div>
            )}

            {ongletActif === 1 && (
                <div className="bg-surface-card rounded-card border border-border overflow-hidden shadow-sm">
                    <table className="w-full text-sm">
                        <thead>
                        <tr className="text-left text-xs text-muted bg-surface border-b border-border">
                            <th className="px-4 py-2.5 font-medium">Date</th>
                            <th className="px-4 py-2.5 font-medium">Statut</th>
                            <th className="px-4 py-2.5 font-medium">Progression</th>
                        </tr>
                        </thead>
                        <tbody>
                        {visites?.results?.map((v) => (
                            <tr
                                key={v.id}
                                onClick={() => navigate(`/visites/${v.id}`)}
                                className="border-b border-border last:border-0 hover:bg-surface cursor-pointer transition-colors duration-200"
                            >
                                <td className="px-4 py-2.5 text-body">{v.date_visite}</td>
                                <td className="px-4 py-2.5">
                    <span className={`px-2 py-0.5 rounded-full text-xs ${STATUT_STYLES[v.statut]}`}>
                      {STATUT_LABELS[v.statut]}
                    </span>
                                </td>
                                <td className="px-4 py-2.5 text-muted">{v.avancement}%</td>
                            </tr>
                        ))}
                        {!visitesLoading && !visites?.results?.length && (
                            <tr>
                                <td colSpan={3} className="px-4 py-8 text-center text-muted">
                                    Aucune visite pour cet établissement pour l'instant.
                                </td>
                            </tr>
                        )}
                        </tbody>
                    </table>
                </div>
            )}
        </Layout>
    )
}

function Champ({ label, valeur }: { label: string; valeur: string }) {
    return (
        <div>
            <dt className="text-xs text-muted mb-0.5">{label}</dt>
            <dd className="text-body">{valeur}</dd>
        </div>
    )
}