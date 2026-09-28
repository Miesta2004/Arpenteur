import type { StatutEtablissement, StatutVisite } from '@/api/types'

export const STATUT_LABELS: Record<StatutVisite, string> = {
  brouillon: 'Brouillon',
  en_cours: 'En cours',
  termine: 'Terminé',
  envoye: 'Validé', // valeur technique historique, libellé renommé (Partie 3 du dossier)
}

// Couleurs sémantiques de la charte (§11 : vert = progression, bleu = information,
// orange = attention). "Brouillon" n'est pas un des 4 états officiels de la charte,
// donc traité en neutre plutôt qu'en état sémantique.
export const STATUT_STYLES: Record<StatutVisite, string> = {
  brouillon: 'bg-border text-muted',
  en_cours: 'bg-info/10 text-info',
  termine: 'bg-warning/10 text-warning',
  envoye: 'bg-success/10 text-success',
}

export const STATUT_ETABLISSEMENT_LABELS: Record<StatutEtablissement, string> = {
  actif: 'Actif',
  inactif: 'Inactif',
  ferme: 'Fermé',
}

export const STATUT_ETABLISSEMENT_STYLES: Record<StatutEtablissement, string> = {
  actif: 'bg-success/10 text-success',
  inactif: 'bg-warning/10 text-warning',
  ferme: 'bg-danger/10 text-danger',
}
