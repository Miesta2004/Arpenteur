import { useState } from 'react'
import type { Batiment, Chambre, Etage, Etablissement, Unite, Zone } from '@/api/types'
import { ChevronRight, Building2, Layers, Users, LayoutGrid, DoorOpen } from 'lucide-react'

export type StatutZone = 'complete' | 'estimation' | 'non_visitee' | 'partielle'

export const STATUT_ZONE_STYLES: Record<StatutZone, string> = {
    complete: 'bg-success',
    partielle: 'bg-warning',
    estimation: 'bg-info',
    non_visitee: 'bg-border',
}

export const STATUT_ZONE_LABELS: Record<StatutZone, string> = {
    complete: 'Complète',
    partielle: 'Partielle',
    estimation: 'Estimation',
    non_visitee: 'Non visitée',
}

function statutZone(zone: Zone): StatutZone {
    if (zone.a_detail) return 'complete'
    if (zone.nb_chambres_estime != null) return 'estimation'
    if (zone.derniere_visite_maj == null) return 'non_visitee'
    return 'partielle'
}

// --- Nœud générique : gère lui-même son expand/collapse ---
function Noeud({
                   icone: Icone,
                   label,
                   sousLabel,
                   enfants,
                   ouvertParDefaut = false,
               }: {
    icone: typeof Building2
    label: string
    sousLabel?: React.ReactNode
    enfants?: React.ReactNode
    ouvertParDefaut?: boolean
}) {
    const [ouvert, setOuvert] = useState(ouvertParDefaut)
    const aDesEnfants = !!enfants

    return (
        <div>
            <button
                onClick={() => aDesEnfants && setOuvert(!ouvert)}
                className={`flex items-center gap-1.5 w-full text-left py-1.5 px-2 rounded-button hover:bg-surface transition-colors duration-200 ${
                    aDesEnfants ? 'cursor-pointer' : 'cursor-default'
                }`}
            >
                {aDesEnfants ? (
                    <ChevronRight
                        size={14}
                        className={`text-muted shrink-0 transition-transform duration-200 ${ouvert ? 'rotate-90' : ''}`}
                    />
                ) : (
                    <span className="w-3.5 shrink-0" />
                )}
                <Icone size={15} className="text-accent shrink-0" />
                <span className="text-sm text-body">{label}</span>
                {sousLabel}
            </button>
            {aDesEnfants && ouvert && <div className="ml-5 border-l border-border pl-2">{enfants}</div>}
        </div>
    )
}

function NoeudChambre({ chambre }: { chambre: Chambre }) {
    const badges = [
        chambre.specialite !== 'generale' ? chambre.specialite_display : null,
        chambre.niveau_confort !== 'standard' ? chambre.niveau_confort_display : null,
    ].filter(Boolean)

    return (
        <Noeud
            icone={DoorOpen}
            label={`${chambre.type_piece_display} ${chambre.numero}`}
            sousLabel={
                badges.length > 0 && (
                    <span className="flex gap-1 ml-1">
            {badges.map((b) => (
                <span key={b} className="px-1.5 py-0.5 rounded-full text-[10px] bg-accent/10 text-accent">
                {b}
              </span>
            ))}
          </span>
                )
            }
        />
    )
}

function NoeudUnite({ unite }: { unite: Unite }) {
    return (
        <Noeud
            icone={LayoutGrid}
            label={unite.nom}
            enfants={
                unite.chambres?.length ? (
                    <>
                        {unite.chambres.map((c) => (
                            <NoeudChambre key={c.id} chambre={c} />
                        ))}
                    </>
                ) : undefined
            }
        />
    )
}

function NoeudZone({ zone }: { zone: Zone }) {
    const statut = statutZone(zone)
    const aDuContenu = (zone.unites?.length ?? 0) > 0 || (zone.chambres?.length ?? 0) > 0

    return (
        <Noeud
            icone={Users}
            label={zone.nom}
            sousLabel={
                <span
                    className={`w-1.5 h-1.5 rounded-full ml-1.5 shrink-0 ${STATUT_ZONE_STYLES[statut]}`}
                    title={STATUT_ZONE_LABELS[statut]}
                />
            }
            enfants={
                aDuContenu ? (
                    <>
                        {zone.unites?.map((u) => (
                            <NoeudUnite key={u.id} unite={u} />
                        ))}
                        {zone.chambres?.map((c) => (
                            <NoeudChambre key={c.id} chambre={c} />
                        ))}
                    </>
                ) : undefined
            }
        />
    )
}

function NoeudEtage({ etage }: { etage: Etage }) {
    return (
        <Noeud
            icone={Layers}
            label={etage.nom}
            enfants={
                etage.zones?.length ? (
                    <>
                        {etage.zones.map((z) => (
                            <NoeudZone key={z.id} zone={z} />
                        ))}
                    </>
                ) : undefined
            }
        />
    )
}

function NoeudBatiment({ batiment }: { batiment: Batiment }) {
    return (
        <Noeud
            icone={Building2}
            label={batiment.nom}
            ouvertParDefaut
            enfants={
                batiment.etages?.length ? (
                    <>
                        {batiment.etages.map((e) => (
                            <NoeudEtage key={e.id} etage={e} />
                        ))}
                    </>
                ) : undefined
            }
        />
    )
}

export default function ArborescenceCartographie({ etablissement }: { etablissement: Etablissement }) {
    const aDuContenu = (etablissement.batiments?.length ?? 0) > 0 || (etablissement.zones_sans_etage?.length ?? 0) > 0

    return (
        <div className="bg-surface-card rounded-card border border-border p-4 shadow-sm">
            {aDuContenu ? (
                <>
                    {etablissement.batiments?.map((b) => (
                        <NoeudBatiment key={b.id} batiment={b} />
                    ))}
                    {etablissement.zones_sans_etage?.map((z) => (
                        <NoeudZone key={z.id} zone={z} />
                    ))}
                </>
            ) : (
                <p className="text-sm text-muted p-4 text-center">
                    Aucune cartographie enregistrée pour cet établissement pour l'instant.
                </p>
            )}
        </div>
    )
}