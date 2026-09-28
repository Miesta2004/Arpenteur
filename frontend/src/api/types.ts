export type StatutVisite = 'brouillon' | 'en_cours' | 'termine' | 'envoye'
export type TypeVisite = 'initiale' | 'suivi'

export type TypePiece =
    | 'chambre_patient'
    | 'consultation'
    | 'bureau_medecin'
    | 'operation'
    | 'accueil_attente'
    | 'toilettes'
    | 'stock'
    | 'technique_informatique'
    | 'autre'

export type CategorieChambre = 'commune' | 'double' | 'individuelle' | 'suite'
export type SpecialiteChambre =
    | 'generale' | 'isolement' | 'reanimation' | 'soins_intensifs'
    | 'maternite' | 'pediatrie' | 'psychiatrie'
export type NiveauConfort = 'standard' | 'confort' | 'premium' | 'vip'

// État CONSTATÉ À LA DERNIÈRE VISITE d'audit — pas un suivi live de l'occupation
// patient (Arpenteur ne gère jamais les patients). Voir derniere_visite_maj.
export type EtatLit = 'disponible' | 'occupe' | 'reserve' | 'en_nettoyage' | 'en_maintenance' | 'hors_service'

export type CategorieEquipement = 'medical' | 'informatique' | 'mobilier' | 'autre'
export type EtatEquipement = 'fonctionnel' | 'en_panne' | 'a_verifier'
// Même logique que EtatLit : constaté à la dernière visite, pas suivi live.
export type DisponibiliteEquipement = 'disponible' | 'en_utilisation' | 'reserve' | 'indisponible'

export interface Caracteristique {
  id: number
  code: string
  label: string
  categorie: string
  ordre: number
}

export interface Lit {
  id: number
  chambre: number
  identifiant: string
  etat: EtatLit
  etat_display: string
  est_utilisable: boolean
  equipements: string
  derniere_visite_maj: number | null
}

export interface MaintenanceEquipement {
  id: number
  equipement: number
  type_intervention: 'preventive' | 'corrective'
  type_intervention_display: string
  date: string
  technicien: string
  description: string
  prochain_controle: string | null
}

export interface Equipement {
  id: number
  nom: string
  categorie: CategorieEquipement
  etat: EtatEquipement
  disponibilite: DisponibiliteEquipement
  disponibilite_display: string
  numero_inventaire: string
  lit: number | null
  chambre: number | null
  zone: number | null
  interventions?: MaintenanceEquipement[]
}

export interface Chambre {
  id: number
  zone: number
  unite: number | null
  numero: string
  type_piece: TypePiece
  type_piece_display: string
  categorie_chambre: CategorieChambre
  categorie_chambre_display: string
  specialite: SpecialiteChambre
  specialite_display: string
  niveau_confort: NiveauConfort
  niveau_confort_display: string
  caracteristiques: Caracteristique[]
  avec_lits: boolean
  capacite_prevue: number | null
  notes: string
  derniere_visite_maj: number | null
  lits?: Lit[]
  equipements_lies?: Equipement[]
}

export interface Unite {
  id: number
  zone: number
  nom: string
  description: string
  ordre: number
  derniere_visite_maj: number | null
  chambres?: Chambre[]
}

export interface Zone {
  id: number
  etablissement: number
  etage_obj: number | null
  etage_libre: string
  nom: string
  type: string
  nb_chambres_estime: number | null
  nb_lits_estime: number | null
  a_detail: boolean
  derniere_visite_maj: number | null
  // chambres : uniquement celles SANS unité (mode rapide) — celles rattachées à
  // une Unité apparaissent sous unites[].chambres, jamais les deux à la fois.
  chambres?: Chambre[]
  unites?: Unite[]
}

export interface Etage {
  id: number
  batiment: number
  nom: string
  description: string
  ordre: number
  derniere_visite_maj: number | null
  zones?: Zone[]
}

export interface Batiment {
  id: number
  etablissement: number
  nom: string
  usage_principal: string
  nb_etages_declare: number | null
  etat_general: string
  ordre: number
  derniere_visite_maj: number | null
  etages?: Etage[]
}

export type StatutEtablissement = 'actif' | 'inactif' | 'ferme'

export interface Etablissement {
  id: number
  nom: string
  type: string
  statut: StatutEtablissement
  ville: string
  region: string
  adresse?: string
  latitude?: string | null
  longitude?: string | null
  contact_nom?: string
  contact_telephone?: string
  contact_email?: string
  derniere_visite_date?: string | null
  // Présents seulement sur le détail (GET /etablissements/{id}/), pas sur la liste :
  batiments?: Batiment[]
  zones_sans_etage?: Zone[]
  nb_batiments?: number
  nb_etages?: number
  nb_services?: number
  nb_chambres?: number
  nb_lits?: number
  nb_equipements?: number
}

export interface Commentaire {
  id: number
  visite: number
  auteur: { id: number; username: string; first_name: string; last_name: string; email: string } | null
  texte: string
  date_creation: string
}

export interface MembreEquipe {
  id: number
  visite: number
  utilisateur: { id: number; username: string; first_name: string; last_name: string; email: string }
  est_inspecteur_principal: boolean
}

export interface Visite {
  id: number
  etablissement: number
  etablissement_nom?: string
  date_visite: string
  statut: StatutVisite
  type_visite: TypeVisite
  avancement: number
  // Comptent ce que CETTE visite a créé/mis à jour (derniere_visite_maj), pas l'état
  // global de l'établissement — voir la discussion sur la structure partagée.
  nb_batiments?: number
  nb_zones?: number
  nb_chambres?: number
  nb_lits?: number
  // Présents seulement sur le détail (GET /visites/{id}/) :
  auteur?: string
  etat_locaux?: string
  reseau_disponible?: boolean
  wifi_disponible?: boolean
  observations_it?: string
  effectif_medecins?: number | null
  effectif_infirmiers?: number | null
  effectif_autres?: number | null
  processus_actuels?: string
  priorites_contraintes?: string
  membres_equipe?: MembreEquipe[]
  commentaires?: Commentaire[]
}

export interface TableauDeBord {
  nb_etablissements: number
  nb_visites: number
  nb_visites_en_cours: number
  nb_rapports_generes: number
  visites_recentes: Visite[]
}

export interface PaginatedResponse<T> {
  count: number
  next: string | null
  previous: string | null
  results: T[]
}
