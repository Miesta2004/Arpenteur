import type { Etablissement } from '@/api/types'
import { Building2, Layers, Users, DoorOpen, BedDouble, Wrench } from 'lucide-react'

const RESUME_ITEMS = [
    { key: 'nb_batiments', label: 'Bâtiments', icon: Building2 },
    { key: 'nb_etages', label: 'Étages', icon: Layers },
    { key: 'nb_services', label: 'Services', icon: Users },
    { key: 'nb_chambres', label: 'Chambres', icon: DoorOpen },
    { key: 'nb_lits', label: 'Lits', icon: BedDouble },
    { key: 'nb_equipements', label: 'Équipements', icon: Wrench },
] satisfies { key: keyof Etablissement; label: string; icon: typeof Building2 }[]

export default function ResumeCartographie({ etablissement }: { etablissement: Etablissement }) {
    return (
        <div className="bg-surface-card rounded-card border border-border p-6 shadow-sm h-fit">
            <h2 className="text-sm font-semibold text-title mb-4">Résumé</h2>
            <div className="grid grid-cols-2 gap-4">
                {RESUME_ITEMS.map(({ key, label, icon: Icon }) => (
                    <div key={key} className="flex items-center gap-2.5">
                        <div className="w-8 h-8 rounded-button bg-accent/10 flex items-center justify-center shrink-0">
                            <Icon size={15} className="text-accent" />
                        </div>
                        <div>
                            <div className="text-sm font-semibold text-title">{(etablissement[key] as number) ?? 0}</div>
                            <div className="text-xs text-muted">{label}</div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    )
}