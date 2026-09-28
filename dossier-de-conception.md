# PARTIE 1
# Vision du Produit
## config — Dossier de Conception

---

# Introduction

Ce document ouvre le dossier de conception d'**config**.

Il fixe le cadre avant toute décision d'architecture ou de code.

Toutes les parties suivantes du dossier s'appuieront sur cette vision.

Si une fonctionnalité future ne sert pas cette vision, elle ne doit pas être ajoutée.

---

# Pourquoi config existe

Avant de déployer un logiciel de gestion hospitalière comme HealthTracker, il faut d'abord **connaître le terrain**.

Aujourd'hui, ce travail de connaissance se fait :

- sur papier ;
- dans des fichiers Excel dispersés ;
- dans la mémoire de quelques personnes ;
- ou pas du tout.

Résultat : chaque déploiement redémarre de zéro.

Chaque audit reprend les mêmes questions.

Chaque établissement réinvente sa propre façon de décrire ses locaux, son matériel, son personnel.

**config existe pour remplacer cette improvisation par une méthode répétable.**

Un outil unique, structuré, qui accompagne la personne sur le terrain — pendant une visite — et transforme ce qu'elle observe en données exploitables.

---

# Le problème qu'config résout

Trois problèmes concrets, dans l'ordre où ils se posent sur le terrain.

## 1. La collecte d'information est non structurée

Chaque visiteur note ce qu'il veut, comme il veut.

Deux visites du même établissement, faites par deux personnes différentes, ne se ressemblent pas.

Rien n'est comparable, rien n'est réutilisable.

## 2. Le niveau de détail nécessaire varie selon le contexte

Parfois, il suffit de savoir qu'un service a « environ 20 lits ».

Parfois, il faut savoir précisément que la chambre 204 a deux lits, dont un avec prise d'oxygène.

Un outil qui impose un seul niveau de détail échoue dans un des deux cas.

## 3. L'information recueillie doit pouvoir être réutilisée sans ressaisie

Une visite terrain n'a de valeur que si elle sert ensuite : à produire un rapport, à préparer un déploiement, à alimenter un logiciel de gestion.

Si les données restent captives d'un PDF ou d'un carnet, la visite n'a servi qu'une fois.

---

# Ce qu'config n'est pas

Pour éviter toute ambiguïté dans les parties suivantes de ce dossier :

- config n'est **pas** un logiciel de gestion hospitalière. Il ne gère ni patients, ni admissions, ni dossiers médicaux. C'est le rôle du SIH (HealthTracker).
- config n'est **pas** un outil de supervision temps réel. Il photographie un état à un instant donné (une visite), il ne suit pas une activité en continu.
- config n'est **pas** réservé aux hôpitaux, mais il n'est pas non plus un outil générique de gestion de patrimoine immobilier. Son cœur reste le recensement et l'audit d'un site de santé, avec une porte ouverte vers des structures voisines (cliniques, laboratoires, postes de santé).

Cette distinction protège config d'un risque simple : devenir, avec le temps, un mauvais clone de HealthTracker au lieu de rester un outil de terrain excellent dans son rôle propre.

---

# À qui config est destiné

## Utilisateur principal : la personne en visite

Consultant, technicien, chargé de déploiement, auditeur — la personne qui se déplace physiquement dans l'établissement, visite après visite, et remplit config pendant ou juste après sa visite.

Ce qu'elle attend :

- un formulaire qui suit sa logique de visite, pas la logique d'une base de données ;
- la possibilité d'aller vite quand le temps manque, et dans le détail quand il en faut ;
- un livrable immédiat (le rapport) à la fin de sa visite.

## Utilisateur secondaire : le commanditaire de la visite

Direction d'établissement, responsable de projet côté bailleur ou côté ministère, futur exploitant de HealthTracker.

Ce qu'il attend :

- un rapport lisible, qui ne nécessite pas de comprendre config pour être utile ;
- une preuve que l'état des lieux a été fait sérieusement ;
- à terme, une passerelle vers le déploiement du SIH, sans ressaisie.

## Utilisateur futur : l'équipe de déploiement du SIH

Celui qui, une fois la visite validée, doit configurer HealthTracker pour cet établissement.

Ce qu'il attend (vision long terme, pas une exigence immédiate) :

- récupérer la structure du bâtiment (bâtiments, étages, services, chambres, lits) sans la ressaisir ;
- s'appuyer sur l'audit IT et l'audit des effectifs pour calibrer le déploiement.

---

# Comment config s'intègre avec le SIH

Ce point mérite d'être posé clairement dès cette première partie, car c'est une source récurrente de confusion.

## Ce qui est vrai aujourd'hui

config est **autonome**. Il fonctionne, sert, et produit de la valeur (rapport de visite) sans qu'HealthTracker existe ou soit déployé quelque part.

## Ce qui est vrai à terme

config devient la **porte d'entrée des données physiques** du SIH.

```
config                              HealthTracker

Visite terrain
      │
      ▼
Recensement                            (rien, pour l'instant)
(bâtiments, étages,
 services, chambres,
 lits, équipements)
      │
      ▼
Visite validée
      │
      ▼
Export  ─────────────────────────▶     Import
                                        Création automatique de :
                                        établissement, bâtiments,
                                        étages, services, chambres,
                                        lits, équipements
```

## Ce qui reste à décider plus tard, pas maintenant

- Le format exact de l'échange (API REST déjà présente côté config, à consommer côté HealthTracker le moment venu).
- Le moment où HealthTracker aura lui-même besoin d'un modèle Bâtiment/Étage/Chambre/Lit pour recevoir ces données (voir `vision-et-etapes.md`, étape A).
- La question de la synchronisation continue (si l'établissement change après la visite, qui met à jour quoi).

**Principe directeur pour tout le reste du dossier** : config se conçoit et se construit pour être excellent seul. L'intégration SIH est une conséquence de cette qualité, pas une condition.

---

# Le principe de gradation

Un principe transversal, qui reviendra dans plusieurs parties du dossier (modèle de données, parcours utilisateur, cartographie) :

**Chaque niveau de détail est optionnel et se rajoute sans tout casser.**

Une visite peut rester à un niveau global (« ce service a environ 20 lits ») ou descendre jusqu'au lit précis avec ses équipements — au choix du visiteur, selon le temps et le besoin disponibles.

Ce principe existe déjà dans le code actuel (`Zone.a_detail`, estimation vs détail réel) et doit être préservé et étendu à mesure qu'config grandit — pas remplacé par un modèle qui impose un seul niveau de saisie.

---

# Ce qu'config pourrait devenir (vision élargie, non prioritaire)

Le modèle de recensement (bâtiment → étage → service → chambre → lit → équipement) n'est pas spécifique à un hôpital.

À long terme, et **seulement si le besoin se confirme**, config pourrait servir pour :

- les cliniques privées ;
- les laboratoires ;
- les postes de santé ;
- d'autres bâtiments complexes hors du secteur santé.

Cette extension n'est **pas un objectif de conception à satisfaire dès maintenant**. Elle influence une seule chose dans ce dossier : éviter de nommer les choses de façon trop spécifique à l'hôpital dans le modèle de données (partie 3), pour ne pas avoir à tout renommer plus tard. Elle ne justifie aucune fonctionnalité, aucun écran, aucun module supplémentaire à ce stade.

---

# Ce qui ne change pas par rapport à l'existant

Ce dossier de conception vient s'ajouter à ce qui existe déjà et fonctionne :

- Le questionnaire en 5 volets (identification, cartographie physique, infrastructure IT, effectifs, processus, priorités).
- La cartographie optionnelle Zone → Chambre → Lit, avec estimation ou détail réel.
- L'export PDF.
- L'API DRF (`/api/zones/`, `/api/chambres/`, `/api/lits/`).

Rien de tout cela n'est remis en cause par ce dossier. Les parties suivantes construisent **autour**, pas à la place.

---

# Ce que cette vision entraîne pour la suite du dossier

Chaque partie suivante devra pouvoir répondre à cette question simple : *est-ce que ceci sert un visiteur de terrain, aujourd'hui, à décrire ce qu'il voit plus vite ou plus fidèlement ?*

Si la réponse est non, la fonctionnalité attend une partie « vision long terme », elle ne rentre pas dans le développement immédiat.

Prochaines parties du dossier :

- **Partie 2** : Architecture fonctionnelle (les modules et leurs rôles).
- **Partie 3** : Modèle de données détaillé.
- **Partie 4** : Parcours utilisateur.
- **Partie 5** : Cahier des charges technique.
- **Partie 6** : UX/UI.
- **Partie 7** : Plan de développement.

---

**Fin de la Partie 1 – Vision du Produit**

**Partie 2 : Architecture fonctionnelle — Tableau de bord, Établissements, Visites, Cartographie, Bâtiments, Étages, Services, Chambres, Lits, Équipements, Photos, Questionnaires, Rapports, Exports, Administration.**
-e 


# PARTIE 2
# Architecture Fonctionnelle
## config — Dossier de Conception

---

# Introduction

Cette partie décrit tous les modules d'config.

Chaque module est décrit selon quatre angles :

- son objectif ;
- ses fonctionnalités ;
- les rôles autorisés à l'utiliser ;
- les écrans associés.

Les modules déjà existants dans le code sont signalés par **[Existant]**.
Les modules à construire sont signalés par **[À construire]**.

---

# Vue d'ensemble des modules

```
config
│
├── Tableau de bord            [À construire]
├── Établissements              [Existant]
├── Visites                     [Existant]
├── Cartographie                [Existant, à faire évoluer]
│     ├── Bâtiments             [À construire]
│     ├── Étages                [À construire]
│     ├── Services              [Existant, sous le nom "Zone"]
│     ├── Chambres              [Existant]
│     └── Lits                  [Existant]
├── Équipements                 [À construire]
├── Photos                      [À construire]
├── Questionnaires               [Existant, intégré à la Visite]
├── Rapports                    [Existant (PDF), à enrichir]
├── Exports                     [Existant (API), à étendre]
└── Administration               [À construire]
```

---

# Rôles (posés ici, détaillés en Partie 5)

Pour éviter de répéter la même liste dans chaque module, on fixe trois rôles de départ :

- **Visiteur** : remplit les visites, la cartographie, ajoute des photos. C'est l'utilisateur principal (voir Partie 1).
- **Responsable de mission** : supervise plusieurs visiteurs, valide les visites, génère les rapports finaux, gère les exports.
- **Administrateur** : gère les comptes, les établissements, les paramètres globaux.

Un seul utilisateur peut cumuler ces rôles dans une petite équipe — ce ne sont pas des comptes séparés obligatoires, mais des permissions.

---

# Module — Tableau de bord

**[À construire]**

## Objectif

Donner une vue d'ensemble immédiate de l'activité, sans avoir à ouvrir chaque établissement un par un.

## Fonctionnalités

- Nombre d'établissements visités, en cours, à visiter.
- Dernières visites modifiées.
- Visites en statut « Brouillon » depuis longtemps (à relancer).
- Raccourci vers « Nouvelle visite ».
- Filtrable par région, par visiteur, par période.

## Rôles autorisés

Visiteur (vue limitée à ses propres visites), Responsable de mission (vue globale), Administrateur (vue globale).

## Écrans associés

- Écran d'accueil après connexion.

---

# Module — Établissements

**[Existant]**

## Objectif

Centraliser les informations qui ne changent pas d'une visite à l'autre : identité de l'établissement, localisation, contact.

## Fonctionnalités actuelles

- Création, consultation d'un établissement.
- Champs : nom, type, statut juridique, ville, région, adresse, contact (nom, fonction, téléphone, email).
- Un établissement peut avoir plusieurs visites dans le temps.

## Fonctionnalités à ajouter (Phase 1 du plan reçu)

- Coordonnées GPS.
- Photo de l'établissement (façade).
- Niveau d'avancement global (calculé à partir du statut des visites).

## Rôles autorisés

Visiteur (création, lecture), Responsable de mission (lecture, édition), Administrateur (tout, y compris suppression).

## Écrans associés

- Liste des établissements (`liste_etablissements`, existant).
- Détail d'un établissement (`detail_etablissement`, existant).
- Formulaire de création (`creer_etablissement`, existant).

---

# Module — Visites

**[Existant]**

## Objectif

Représenter une visite terrain unique, à une date donnée, par un auteur donné — le questionnaire complet en 5 volets.

## Fonctionnalités actuelles

- Questionnaire en 5 sections : Identification, Cartographie physique (déclaratif), Infrastructure IT, Effectifs, Processus actuels, Priorités et contraintes.
- Statut : Brouillon / Terminé (bascule simple).
- Duplication d'une visite (recopie la cartographie détaillée pour une visite de suivi).
- Suppression.

## Fonctionnalités à ajouter (Phase 1 du plan reçu)

- Statut étendu : Brouillon → En cours → Terminé → Validé (au lieu du simple bascule actuel).
- Champ commentaires libres visibles indépendamment des sections (déjà en partie couvert par `notes_libres`, à vérifier en Partie 3).
- Niveau d'avancement (pourcentage de sections remplies), affiché pendant la saisie.

## Rôles autorisés

Visiteur (création, édition tant que non Validé), Responsable de mission (validation, passage au statut Validé), Administrateur (tout).

## Écrans associés

- Détail d'une visite (`detail_visite`, existant).
- Formulaire de modification (`modifier_visite`, existant).
- Création (`creer_visite`, existant).

---

# Module — Cartographie

**[Existant, à faire évoluer]**

## Objectif

Représenter la structure physique de l'établissement, du niveau le plus global (bâtiment) au plus fin (lit), avec un niveau de détail libre (voir principe de gradation, Partie 1).

## État actuel

Le code gère aujourd'hui trois niveaux : `Zone` (≈ service), `Chambre`, `Lit`. La hiérarchie Bâtiment → Étage n'existe pas encore ; `Zone` porte un champ `etage` en texte libre.

## Cible (Phase 2 du plan reçu)

Une hiérarchie complète :

```
Établissement
   └── Bâtiment
         └── Étage
               └── Service
                     └── Chambre
                           └── Lit
```

Chaque niveau doit pouvoir être créé directement depuis la visite, sans écran séparé complexe.

## Rôles autorisés

Visiteur (création, édition), Responsable de mission (lecture, édition), Administrateur (tout).

## Écrans associés

- Page cartographie actuelle (`cartographie_visite`), à faire évoluer en Partie 6 (UX/UI) et Partie 4 (parcours).

---

## Sous-module — Bâtiments

**[À construire]**

### Objectif

Regrouper les étages sous un même bâtiment physique, avec sa propre identité (nom, usage principal — ex. « Bloc chirurgie »).

### Fonctionnalités

- Créer un bâtiment rattaché à une visite.
- Nom, nombre d'étages déclaré, usage principal, état général des locaux.

### Écrans associés

- Intégré à la page cartographie (pas d'écran séparé prévu).

---

## Sous-module — Étages

**[À construire]**

### Objectif

Découper un bâtiment en niveaux (RDC, R+1, etc.), chacun pouvant contenir plusieurs services.

### Fonctionnalités

- Créer un étage rattaché à un bâtiment.
- Nom/numéro d'étage, description courte.

### Écrans associés

- Intégré à la page cartographie.

---

## Sous-module — Services

**[Existant, sous le nom « Zone »]**

### Objectif

Décrire une unité fonctionnelle (Urgences, Pédiatrie, Cardiologie...), avec une estimation rapide ou un détail chambre par chambre.

### Fonctionnalités actuelles

- Nom, type, étage (texte libre), estimation (`nb_chambres_estime`, `nb_lits_estime`).
- `a_detail` : vrai si au moins une chambre a été détaillée.

### Évolution prévue

- Rattachement à un `Étage` réel (objet) plutôt qu'à un champ texte libre — voir Partie 3 pour la question de migration des données existantes.
- Renommage progressif `Zone` → `Service` dans l'interface (pas nécessairement dans le code, pour ne pas casser l'existant sans réflexion — voir Partie 3).

### Écrans associés

- Page cartographie.

---

## Sous-module — Chambres

**[Existant]**

### Objectif

Détailler une pièce précise : son numéro, sa capacité prévue, et ses lits.

### Fonctionnalités actuelles

- Numéro, capacité prévue, rattachement à une `Zone`.

### Écrans associés

- Page cartographie.

---

## Sous-module — Lits

**[Existant]**

### Objectif

Le niveau le plus fin du recensement : un lit identifié, avec ses équipements déclarés en texte libre.

### Fonctionnalités actuelles

- Identifiant (unique par chambre), équipements (texte libre).

### Évolution prévue

- Les équipements passent d'un champ texte libre à de vraies fiches (voir module Équipements ci-dessous), sans supprimer la possibilité de rester sommaire si le visiteur n'a pas le temps.

### Écrans associés

- Page cartographie.

---

# Module — Équipements

**[À construire]**

## Objectif

Recenser précisément le matériel présent dans une chambre ou un service : ce qui existe, son état, et des informations d'inventaire utiles à un futur déploiement ou à un audit biomédical.

## Fonctionnalités (Phase 3 du plan reçu)

- Rattachement à un lit, une chambre, ou un service (un équipement n'est pas toujours lié à un lit précis : un défibrillateur peut être partagé sur un service entier).
- Champs : nom/type, numéro d'inventaire, état (fonctionnel / en panne / à vérifier), fabricant, année, photo, observations.
- Comme pour la cartographie, ce module reste **optionnel** : un lit peut très bien n'avoir aucun équipement détaillé (texte libre suffisant) et un autre avoir une fiche complète.

## Rôles autorisés

Visiteur (création, édition), Responsable de mission (lecture), Administrateur (tout).

## Écrans associés

- Intégré à la fiche chambre/lit dans la page cartographie — pas d'écran séparé dans un premier temps.

---

# Module — Photos

**[À construire]**

## Objectif

Illustrer une visite : façade de l'établissement, état d'une chambre, matériel, anomalie constatée. Les photos rendent le rapport crédible et concret.

## Fonctionnalités

- Attachables à : un établissement, une visite, une chambre, un équipement.
- Légende courte obligatoire (pour qu'une photo ait un sens hors contexte, notamment dans le rapport PDF).
- Pas de limite technique arbitraire de nombre de photos, mais une recommandation d'usage (photos utiles, pas exhaustives) posée en Partie 6.

## Rôles autorisés

Visiteur (ajout), Responsable de mission (lecture, suppression), Administrateur (tout).

## Écrans associés

- Intégrées aux écrans établissement, visite, cartographie.
- Galerie photo dans le rapport PDF (Partie 6).

---

# Module — Questionnaires

**[Existant, intégré à la Visite]**

## Objectif

Ce module n'est pas séparé dans le code actuel : c'est le corps même du formulaire `Visite` (les 5 sections). On le documente séparément ici pour clarté, mais il ne s'agit pas de le sortir en module technique indépendant sans raison.

## Fonctionnalités actuelles

Voir module Visites ci-dessus — c'est la même chose.

## Point de vigilance

Le plan reçu liste « Questionnaires » comme un module à part entière. Après analyse, il n'y a pas de bénéfice à le séparer techniquement de `Visite` : ce serait une complexité ajoutée sans fonctionnalité nouvelle. Ce point sera tranché définitivement en Partie 3 (modèle de données).

## Écrans associés

Identiques au module Visites.

---

# Module — Rapports

**[Existant (PDF), à enrichir]**

## Objectif

Produire le livrable final d'une visite : un document lisible par quelqu'un qui n'a pas utilisé config.

## Fonctionnalités actuelles

- Export PDF d'une visite, incluant la cartographie déclarée.

## Fonctionnalités à ajouter (Phase 6 du plan reçu)

- Résumé en première page (synthèse en quelques lignes, pas juste des données brutes).
- Statistiques (occupation estimée, répartition des lits par service).
- Section anomalies (constats négatifs signalés pendant la visite — état des locaux dégradé, matériel en panne).
- Section recommandations (rédigées par le responsable de mission, pas générées automatiquement).
- Galerie photo.

## Rôles autorisés

Visiteur (génération), Responsable de mission (génération, édition des recommandations avant génération finale), Administrateur (tout).

## Écrans associés

- Bouton d'export depuis le détail de visite (existant).
- Pas d'écran de rapport en ligne dans un premier temps : le PDF reste le format de référence.

---

# Module — Exports

**[Existant (API), à étendre]**

## Objectif

Permettre à un système tiers (au premier chef, HealthTracker) de consommer les données d'config sans ressaisie.

## Fonctionnalités actuelles

- API DRF : `/api/zones/`, `/api/chambres/`, `/api/lits/` (lecture et écriture, utilisée aujourd'hui par la page cartographie elle-même).

## Fonctionnalités à ajouter (Phase 7 du plan reçu — vision long terme, pas immédiate)

- Export JSON complet d'une visite validée (établissement, bâtiments, étages, services, chambres, lits, équipements).
- Point d'entrée pensé pour être consommé par un import côté SIH, le jour où ce dernier en a besoin (voir `vision-et-etapes.md`).

## Rôles autorisés

Responsable de mission (déclenche l'export), Administrateur (configure les destinations d'export).

## Écrans associés

- Bouton d'export sur une visite validée (à ajouter, Partie 6).

---

# Module — Administration

**[À construire]**

## Objectif

Gérer ce qui ne relève pas d'une visite en particulier : comptes utilisateurs, rôles, paramètres globaux.

## Fonctionnalités

- Gestion des comptes (création, désactivation) et de leur rôle (Visiteur / Responsable de mission / Administrateur).
- Paramétrage des listes de choix utilisées dans les formulaires (types d'établissement, types d'équipement) pour éviter de coder en dur des valeurs qui évolueront.
- Journal d'activité minimal (qui a créé/modifié/validé quoi — utile dès qu'il y a plusieurs visiteurs).

## Rôles autorisés

Administrateur uniquement (à l'exception de la consultation du journal, ouverte au Responsable de mission).

## Écrans associés

- Django Admin peut couvrir une bonne partie de ce besoin au départ (déjà utilisé pour `Etablissement`, `Visite`, etc. — voir `admin.py`), avant de justifier une interface dédiée.

---

# Ce que cette partie n'a pas tranché (renvoyé aux parties suivantes)

- La structure exacte des tables et leurs relations → **Partie 3**.
- L'ordre exact dans lequel un visiteur navigue entre ces modules → **Partie 4**.
- Les choix techniques (PostgreSQL, cartographie SVG, authentification) → **Partie 5**.
- Le détail des écrans → **Partie 6**.
- L'ordre de développement réel, module par module → **Partie 7**.

---

**Fin de la Partie 2 – Architecture Fonctionnelle**

**Partie 3 : Modèle de données détaillé — entités, champs, relations, migration depuis le modèle existant.**
-e 


# PARTIE 3
# Modèle de Données Détaillé
## config — Dossier de Conception

---

# Introduction

Cette partie décrit toutes les entités du modèle de données cible, leurs champs, leurs relations, et surtout **comment on passe du modèle actuel (`models.py`) à ce modèle cible sans tout casser**.

Principe directeur, hérité de la Partie 1 : chaque évolution doit être **additive**. Les visites déjà saisies avec le modèle actuel doivent continuer à fonctionner pendant et après la migration.

---

# Vue d'ensemble — schéma relationnel cible

```
Etablissement
     │
     │ 1,n
     ▼
   Visite
     │
     │ 1,n
     ▼
  Batiment
     │
     │ 1,n
     ▼
   Etage
     │
     │ 1,n
     ▼
   Service  (= Zone actuel, renommé progressivement)
     │
     │ 1,n
     ▼
  Chambre
     │
     │ 1,n
     ▼
    Lit
     │
     │ 0,n
     ▼
 Equipement ◀── aussi rattachable directement à Chambre ou Service

  Photo  ──▶ rattachable à Etablissement, Visite, Chambre ou Equipement

Utilisateur ──▶ auteur d'une Visite, propriétaire de permissions (Rôle)

JournalActivite ──▶ trace les actions sur Visite, Batiment...Equipement
```

---

# 1. Etablissement

**Existant — pas de changement de structure, deux champs à ajouter.**

| Champ | Type | Statut |
|---|---|---|
| nom | CharField(200) | existant |
| type | CharField, choix | existant |
| statut_juridique | CharField, choix | existant |
| ville | CharField(100) | existant |
| region | CharField(100) | existant |
| adresse | CharField(255) | existant |
| contact_nom / contact_fonction / contact_telephone / contact_email | — | existant |
| date_creation | DateTimeField | existant |
| **latitude, longitude** | DecimalField, nullable | **à ajouter** (Phase 1 du plan) |
| **photo_facade** | ImageField, nullable | **à ajouter**, via le module Photo (voir §9) |

Aucune migration de données nécessaire : ajout de deux champs nullable.

---

# 2. Visite

**Existant — extension du statut, ajout d'un champ d'avancement calculé.**

| Champ | Type | Statut |
|---|---|---|
| etablissement | ForeignKey → Etablissement | existant |
| auteur | CharField(150) | existant — **voir migration vers `Utilisateur` en §8** |
| date_visite | DateField | existant |
| statut | CharField, choix | **existant mais valeurs à étendre** |
| possede_urgences / bloc_operatoire / laboratoire / pharmacie / imagerie | BooleanField | existant |
| etat_locaux | CharField, choix | existant |
| *(tous les champs IT, effectifs, processus, priorités listés en Partie 2)* | — | existant, inchangés |
| date_creation / date_modification | DateTimeField | existant |

## Évolution du statut

Actuellement : `StatutVisite` = Brouillon / Terminé / Envoyé.

Cible (Phase 1 du plan reçu) : Brouillon → En cours → Terminé → Validé.

**Décision de migration** : on ne supprime pas `Envoyé`, on l'aligne avec `Validé` (renommage d'étiquette, la valeur technique `envoye` reste en base pour ne pas casser les visites existantes déjà marquées ainsi). On ajoute `en_cours` entre `brouillon` et `termine`.

```python
class StatutVisite(models.TextChoices):
    BROUILLON = 'brouillon', 'Brouillon'
    EN_COURS  = 'en_cours',  'En cours'
    TERMINE   = 'termine',   'Terminé'
    ENVOYE    = 'envoye',    'Validé'   # libellé renommé, valeur technique conservée
```

## Avancement (nouveau, calculé — pas de champ stocké)

Une `@property` (comme `nb_zones`, `nb_chambres`, `nb_lits` existants) qui calcule le pourcentage de sections remplies. Aucune migration nécessaire : c'est du code, pas une colonne.

---

# 3. Batiment *(nouveau)*

| Champ | Type | Notes |
|---|---|---|
| visite | ForeignKey → Visite, related_name `batiments` | |
| nom | CharField(150) | Ex. « Bloc A », « Bâtiment principal » |
| usage_principal | CharField(150), blank | Ex. « Chirurgie » |
| nb_etages_declare | PositiveIntegerField, nullable | estimation rapide, même logique que `Zone.nb_chambres_estime` |
| etat_general | CharField, choix (réutilise `EtatLocaux`) | |
| ordre | PositiveIntegerField, default 0 | pour l'affichage dans la cartographie |

Rattaché à `Visite` (pas à `Etablissement`) : un bâtiment peut avoir changé entre deux visites (extension, démolition), donc il appartient à l'état constaté à un instant donné — cohérent avec le fait qu'une `Visite` entière est déjà un instantané.

---

# 4. Etage *(nouveau)*

| Champ | Type | Notes |
|---|---|---|
| batiment | ForeignKey → Batiment, related_name `etages` | |
| nom | CharField(50) | Ex. « RDC », « R+1 » |
| description | TextField, blank | |
| ordre | PositiveIntegerField, default 0 | |

---

# 5. Service *(renommage progressif de `Zone`)*

**C'est le point de migration le plus sensible du dossier. Traité avec précaution ci-dessous.**

## Ce qui ne change pas

Tous les champs actuels de `Zone` sont conservés à l'identique : `nom`, `type`, `description`, `ordre`, `nb_chambres_estime`, `nb_lits_estime`, `taux_occupation_pct`, ainsi que les propriétés calculées (`nb_chambres_detaillees`, `a_detail`, etc.).

## Ce qui change

| Champ | Avant | Après |
|---|---|---|
| étage | `etage` (CharField libre) | `etage` devient une **ForeignKey → Etage**, nullable |
| rattachement | `visite` (ForeignKey directe) | **conservé en parallèle** de la nouvelle hiérarchie (voir stratégie ci-dessous) |

## Stratégie de migration (le point clé)

On ne remplace pas `visite = ForeignKey(Visite)` par une dépendance obligatoire à `Etage`. À la place :

1. `Zone.visite` reste tel quel — **toujours renseigné**, y compris pour les zones créées via la nouvelle hiérarchie (on le déduit automatiquement : `zone.visite = zone.etage.batiment.visite`).
2. On ajoute `Zone.etage_obj` (ForeignKey → Etage, **nullable**), en parallèle de l'ancien champ texte `etage` (qu'on renomme `etage_libre` pour éviter toute confusion, mais qu'on garde).
3. Une zone peut donc exister de deux façons : rattachée seulement à une visite avec un étage en texte libre (mode rapide, comme aujourd'hui), ou rattachée en plus à un `Etage` réel de la hiérarchie complète (mode structuré).

Cela respecte le **principe de gradation** posé en Partie 1 : le mode rapide actuel continue de fonctionner sans qu'un visiteur soit obligé de créer Bâtiment → Étage avant de pouvoir noter un service.

## Renommage d'interface

Dans les templates et l'API, on peut afficher « Service » au lieu de « Zone » sans renommer la classe Python ni la table — un simple changement de libellés (`verbose_name`). Le renommage du code lui-même (classe `Zone` → `Service`) est reporté à une passe de nettoyage ultérieure, non prioritaire, pour ne pas complexifier la migration avec un renommage de table en plus du reste.

---

# 6. Chambre

**Existant — un seul ajout.**

| Champ | Type | Statut |
|---|---|---|
| zone | ForeignKey → Zone | existant, inchangé |
| numero | CharField(30) | existant |
| capacite_prevue | PositiveIntegerField | existant |
| notes | CharField(255) | existant |

Aucun changement structurel. Les équipements de chambre (climatisation, prise oxygène murale...) passeront par le module Équipement (§7) plutôt que par un nouveau champ ici.

---

# 7. Lit

**Existant — le champ `equipements` (texte libre) est conservé, en complément du nouveau modèle Équipement.**

| Champ | Type | Statut |
|---|---|---|
| chambre | ForeignKey → Chambre | existant |
| identifiant | CharField(10) | existant |
| fonctionnel | BooleanField | existant |
| equipements | CharField(255), texte libre | **existant, conservé tel quel** |

**Décision** : on ne supprime pas le champ texte libre `equipements`. Il reste la façon rapide de noter « oxygène, moniteur » sans créer de fiches détaillées. Le module Équipement (ci-dessous) est un **ajout**, pas un remplacement — encore une fois pour respecter le principe de gradation.

---

# 8. Equipement *(nouveau)*

| Champ | Type | Notes |
|---|---|---|
| lit | ForeignKey → Lit, nullable | un équipement peut ne pas être lié à un lit précis |
| chambre | ForeignKey → Chambre, nullable | équipement partagé dans une chambre |
| zone | ForeignKey → Zone, nullable | équipement partagé dans un service (ex. défibrillateur mobile) |
| nom | CharField(150) | Ex. « Respirateur », « Moniteur ECG » |
| numero_inventaire | CharField(50), blank | |
| etat | CharField, choix : Fonctionnel / En panne / À vérifier | |
| fabricant | CharField(100), blank | |
| annee | PositiveIntegerField, nullable | |
| observations | TextField, blank | |

**Contrainte applicative** (pas une contrainte base de données stricte, pour rester tolérant) : au moins un des trois rattachements (`lit`, `chambre`, `zone`) doit être renseigné. Vérifiée au niveau du formulaire, pas d'une contrainte SQL bloquante — pour ne pas casser un futur import externe imparfait.

---

# 9. Photo *(nouveau)*

| Champ | Type | Notes |
|---|---|---|
| image | ImageField | |
| legende | CharField(255) | **obligatoire** (voir Partie 2 — une photo doit avoir un sens hors contexte) |
| etablissement | ForeignKey, nullable | |
| visite | ForeignKey, nullable | |
| chambre | ForeignKey, nullable | |
| equipement | ForeignKey, nullable | |
| date_ajout | DateTimeField, auto_now_add | |

Même logique de rattachement multiple optionnel que `Equipement`.

---

# 10. Utilisateur et Rôle

## Décision : ne pas créer de modèle `Utilisateur` personnalisé dès maintenant

Django fournit déjà `django.contrib.auth.User`, utilisé nulle part pour l'instant dans le code actuel (`auteur` est un simple `CharField`). Deux options :

**Option retenue** : utiliser `django.contrib.auth.User` tel quel, et ajouter un modèle `Profil` séparé (relation one-to-one) qui porte le rôle métier :

```python
class RoleUtilisateur(models.TextChoices):
    VISITEUR = 'visiteur', 'Visiteur'
    RESPONSABLE = 'responsable', 'Responsable de mission'
    ADMIN = 'admin', 'Administrateur'

class Profil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=15, choices=RoleUtilisateur.choices, default=RoleUtilisateur.VISITEUR)
```

Cette approche évite de remplacer le système d'authentification standard de Django (risque élevé, bénéfice faible) tout en portant les rôles définis en Partie 2.

## Migration du champ `Visite.auteur`

Le champ `auteur` (texte libre) est **conservé**. On ajoute `Visite.cree_par` (ForeignKey → User, nullable), rempli automatiquement pour les nouvelles visites créées après authentification. Les visites existantes gardent seulement leur `auteur` texte, ce qui reste lisible dans les rapports.

---

# 11. JournalActivite *(nouveau, minimal)*

| Champ | Type | Notes |
|---|---|---|
| utilisateur | ForeignKey → User, nullable | |
| action | CharField, ex. « creation », « modification », « validation » | |
| objet_type | CharField | nom du modèle concerné (« Visite », « Batiment »...) |
| objet_id | PositiveIntegerField | |
| description | CharField(255) | résumé lisible, ex. « Visite validée » |
| date | DateTimeField, auto_now_add | |

Volontairement simple (pas de package tiers de type `django-simple-history` à ce stade) : une table plate, écrite explicitement aux points clés (création de visite, changement de statut, suppression). Suffisant pour répondre au besoin de traçabilité posé en Partie 2, sans ajouter de dépendance lourde avant d'en avoir besoin.

---

# Ce qui n'est délibérément pas créé à ce stade

Le plan reçu mentionnait aussi `Salle`, `Document`, `Equipe`, `Mission`. Décision pour cette partie du dossier :

- **`Salle`** : redondant avec `Chambre` tel que le modèle est déjà pensé (une chambre est une salle). Pas de distinction fonctionnelle claire → non retenu, pour éviter deux entités qui se chevauchent.
- **`Document`** : au-delà des photos, aucun besoin concret identifié pour l'instant (documents administratifs scannés ?). Renvoyé en vision long terme, à réévaluer si le besoin apparaît sur le terrain.
- **`Mission`** : toujours non retenu à ce stade — aucun besoin confirmé d'un regroupement de plusieurs visites sous un objectif commun distinct de l'établissement lui-même.

## Révision — `Equipe` finalement retenu

**Correction par rapport à la décision initiale ci-dessus.** La maquette des écrans (voir Partie 6, mise à jour) montre qu'une visite est en réalité menée par un **inspecteur principal + une équipe de plusieurs personnes** — visible sur l'écran « Détail d'une visite » (« Marie Diallo, 2 personnes »). Ce n'est pas un cas marginal, c'est le mode de fonctionnement normal représenté dans la maquette. On revient donc sur le choix initial :

| Champ | Type | Notes |
|---|---|---|
| visite | ForeignKey → Visite, related_name `membres_equipe` | |
| utilisateur | ForeignKey → User | |
| est_inspecteur_principal | BooleanField, default False | un seul membre par visite devrait porter ce booléen — vérifié au niveau applicatif |

`Visite.cree_par` (§10 ci-dessus) reste le champ technique "qui a créé l'enregistrement" ; `est_inspecteur_principal` sur `MembreEquipe` porte le sens métier "qui dirige la visite", qui peut différer (une visite peut être créée par un assistant pour le compte de l'inspecteur, par exemple).

Ce choix suit directement le principe posé en Partie 1 : ne pas construire une entité tant qu'elle ne sert pas un besoin déjà identifié.

---

# Récapitulatif des migrations Django à prévoir

Dans l'ordre logique de dépendances :

1. `Etablissement` : ajout `latitude`, `longitude` (nullable).
2. `Visite` : ajout valeur `en_cours` au choix `statut` ; ajout `cree_par` (FK User, nullable).
3. Nouveau modèle `Batiment` (FK → Visite).
4. Nouveau modèle `Etage` (FK → Batiment).
5. `Zone` : ajout `etage_obj` (FK → Etage, nullable) ; renommage du champ existant `etage` → `etage_libre` (migration de renommage de colonne, sans perte de données).
6. Nouveau modèle `Equipement` (FK nullable vers Lit, Chambre, Zone).
7. Nouveau modèle `Photo` (FK nullable vers Etablissement, Visite, Chambre, Equipement).
8. Nouveau modèle `Profil` (one-to-one → User).
9. Nouveau modèle `JournalActivite`.

Chaque étape est une migration Django indépendante, testable séparément — cohérent avec l'ordre de développement qui sera détaillé en Partie 7.

---

**Fin de la Partie 3 – Modèle de Données Détaillé**

---
---

# PARTIE 4
# Parcours Utilisateur
## config — Dossier de Conception

---

# Introduction

Cette partie décrit le parcours réel d'un visiteur, du login jusqu'à l'export vers le SIH — étape par étape, avec pour chaque étape : ce que l'utilisateur voit, ce qu'il peut faire, et ce qui se passe s'il s'arrête en cours de route.

Le principe de gradation (Partie 1) structure tout ce parcours : à chaque étape, l'utilisateur peut s'arrêter au niveau global et passer à la suite, ou descendre dans le détail.

---

# Vue d'ensemble du parcours

```
Connexion
   │
   ▼
Tableau de bord
   │
   ▼
Sélection ou création d'un Établissement
   │
   ▼
Création d'une Visite
   │
   ▼
Remplissage du questionnaire (5 sections)
   │
   ├──▶ Section Cartographie physique
   │        │
   │        ▼
   │    Recensement (niveau libre) :
   │    Bâtiment → Étage → Service → Chambre → Lit → Équipement
   │        │
   │        ▼
   │    Ajout de photos (à tout moment)
   │
   ▼
Relecture / niveau d'avancement
   │
   ▼
Passage au statut "Terminé"
   │
   ▼
Validation (par le Responsable de mission) → statut "Validé"
   │
   ▼
Génération du rapport PDF
   │
   ▼
Export vers le SIH (optionnel, vision Phase 2/7)
```

---

# Étape 1 — Connexion

**Ce que voit l'utilisateur** : un écran de connexion standard (identifiant / mot de passe).

**Ce qu'il peut faire** : se connecter. Pas d'auto-inscription libre — les comptes sont créés par un Administrateur (module Administration, Partie 2).

**S'il s'arrête ici** : rien n'est perdu, il n'y a encore aucune donnée.

---

# Étape 2 — Tableau de bord

**Ce que voit l'utilisateur** : selon son rôle (Partie 2) —

- un Visiteur voit ses propres visites en cours et récentes ;
- un Responsable de mission ou Administrateur voit l'activité de toute l'équipe.

**Ce qu'il peut faire** : reprendre une visite en brouillon, en créer une nouvelle, ou consulter un établissement déjà visité.

**Point de vigilance UX** (approfondi en Partie 6) : les visites en « Brouillon » depuis longtemps doivent être mises en évidence, pour éviter les visites oubliées à mi-chemin.

---

# Étape 3 — Sélection ou création d'un établissement

**Cas 1 : l'établissement existe déjà** (visite de suivi). L'utilisateur le retrouve dans la liste (recherche par nom ou ville) et enchaîne directement sur la création d'une nouvelle visite.

**Cas 2 : premier passage dans cet établissement.** L'utilisateur crée la fiche établissement (nom, type, ville, contact — Partie 3). Rapide : moins d'une minute, uniquement les champs qui ne dépendent pas de la visite elle-même.

**S'il s'arrête ici** : la fiche établissement reste utilisable seule (contact, localisation) même sans visite associée — cohérent avec le fait qu'`Etablissement` et `Visite` sont deux entités distinctes (Partie 3).

---

# Étape 4 — Création de la visite

**Ce que voit l'utilisateur** : un formulaire minimal pour démarrer — date de la visite, auteur (pré-rempli avec l'utilisateur connecté, voir `Visite.cree_par` en Partie 3).

**Ce qui se passe ensuite** : la visite est créée avec le statut `Brouillon`, et l'utilisateur est redirigé vers le détail de la visite, point d'entrée de toutes les étapes suivantes.

---

# Étape 5 — Remplissage du questionnaire

**Ce que voit l'utilisateur** : les 5 sections du questionnaire (Partie 2), accessibles indépendamment — pas un tunnel obligatoire dans un ordre imposé. Un visiteur peut remplir « Infrastructure IT » avant « Identification » si c'est plus pratique pendant sa visite (par exemple s'il commence par la salle serveur).

**Indicateur d'avancement** : un pourcentage ou une liste de sections cochées, visible en permanence sur l'écran de détail de visite (voir `avancement` calculé, Partie 3).

**S'il s'arrête ici** : la visite reste en `Brouillon`, récupérable à tout moment. Aucune section n'est « perdue » si l'utilisateur ferme l'onglet — chaque section s'enregistre indépendamment (comportement déjà présent dans le code actuel via les formulaires Django existants).

---

# Étape 6 — Recensement physique (cartographie)

C'est la sous-étape la plus longue et la plus structurante du parcours — elle correspond au module Cartographie (Partie 2) et à la hiérarchie du modèle de données (Partie 3).

## Chemin rapide (mode estimation)

L'utilisateur note directement, au niveau Service : « environ 20 lits, 10 chambres ». Terminé en quelques secondes par service. C'est le comportement déjà existant (`nb_chambres_estime`, `nb_lits_estime`).

## Chemin détaillé (mode structuré)

L'utilisateur descend dans la hiérarchie complète :

1. Il crée un **Bâtiment** (nom, usage).
2. Il ajoute un ou plusieurs **Étages**.
3. Sous chaque étage, il ajoute un ou plusieurs **Services**.
4. Sous chaque service, il détaille les **Chambres**.
5. Sous chaque chambre, il détaille les **Lits**.
6. Optionnellement, il ajoute des **Équipements** à un lit, une chambre, ou un service entier.

**Point clé du parcours** : rien n'oblige à finir un niveau avant de passer au suivant, ni à détailler tous les services de la même façon. Un visiteur peut détailler entièrement le service Urgences (chambre par chambre) et laisser le service Consultations en simple estimation. C'est le comportement déjà supporté par `Zone.a_detail` (Partie 3).

## Ajout de photos

À chaque niveau (établissement, visite, chambre, équipement), l'utilisateur peut ajouter une photo avec sa légende, à tout moment du parcours — pas seulement à la fin.

---

# Étape 7 — Relecture et niveau d'avancement

Avant de marquer la visite comme terminée, l'utilisateur consulte une vue de synthèse : sections remplies, nombre de bâtiments/services/chambres/lits recensés, nombre de photos ajoutées.

**Ce qui se passe s'il manque des sections** : rien de bloquant — l'avancement affiche simplement le pourcentage réel. Aucune section n'est « obligatoire » au sens technique (cohérent avec le principe de gradation).

---

# Étape 8 — Passage au statut « Terminé »

**Qui peut le faire** : le Visiteur lui-même, quand il estime sa visite complète.

**Ce que ça change** : la visite n'apparaît plus dans les « brouillons en attente » du tableau de bord, mais reste modifiable — ce n'est pas un verrouillage, juste un changement de statut visuel (voir `StatutVisite`, Partie 3).

---

# Étape 9 — Validation

**Qui peut le faire** : le Responsable de mission (rôle défini en Partie 2), pas le Visiteur lui-même — séparation volontaire pour garantir un regard extérieur avant qu'une visite soit considérée comme définitive.

**Ce que ça change** : statut → `Validé`. Une entrée est ajoutée au `JournalActivite` (Partie 3). Idéalement, la visite validée devient plus difficile à modifier sans laisser de trace (verrouillage souple, détaillé en Partie 5 — pas un verrouillage strict en base, pour ne pas bloquer une correction légitime).

---

# Étape 10 — Génération du rapport PDF

**Qui peut le faire** : Visiteur ou Responsable de mission, à tout moment en fait (pas seulement après validation) — utile pour partager un état d'avancement avant que la visite soit finie.

**Ce que contient le rapport** : voir module Rapports (Partie 2) — résumé, statistiques, cartographie, anomalies, recommandations (ces deux dernières sections n'ayant de sens qu'une fois la visite avancée).

---

# Étape 11 — Export vers le SIH *(vision, pas prioritaire — voir `vision-et-etapes.md`)*

**Condition** : la visite doit être `Validé`.

**Ce que fait l'utilisateur** : déclenche un export JSON structuré (module Exports, Partie 2).

**Ce que ça ne fait pas aujourd'hui** : il n'y a, à ce stade du projet, personne en face pour recevoir cet export — HealthTracker n'a pas encore de modèle Bâtiment/Étage/Chambre/Lit (voir `vision-et-etapes.md`, étape A). Cette étape du parcours est donc documentée pour la cohérence du dossier, mais **non développée tant que le besoin ne se confirme pas côté SIH**.

---

# Parcours secondaire — visite de suivi (établissement déjà connu)

Cas fréquent : un établissement a déjà été visité une première fois, et une nouvelle visite (suivi, mise à jour) est nécessaire.

**Fonctionnalité existante à conserver et mettre en avant dans ce parcours** : la duplication de visite (`dupliquer_visite`, déjà présente dans le code), qui recopie la cartographie détaillée de la visite précédente, pour que le visiteur n'ait qu'à corriger ce qui a changé plutôt que tout ressaisir.

---

# Ce que cette partie n'a pas tranché

- Le détail visuel exact de chaque écran → **Partie 6**.
- Les choix techniques qui rendent ce parcours possible (auth, upload photo, etc.) → **Partie 5**.

---
---

# PARTIE 5
# Cahier des Charges Technique
## config — Dossier de Conception

---

# Introduction

Cette partie fixe les choix techniques. Principe directeur : **rester sur la stack déjà en place**, l'étendre seulement là où le besoin fonctionnel (Parties 2 à 4) l'exige. Pas de changement technique « parce que c'est mieux » sans besoin identifié.

---

# Stack actuelle (confirmée dans le code)

- **Backend** : Django (voir `requirements.txt`, `arpenteur_project/settings.py`).
- **API** : Django REST Framework, déjà utilisé pour `/api/zones/`, `/api/chambres/`, `/api/lits/` (`api_urls.py`, `serializers.py`).
- **Base de données** : à confirmer dans `settings.py` — SQLite en développement. **Décision** : passage à PostgreSQL requis avant toute mise en production réelle (SQLite ne gère pas bien les accès concurrents de plusieurs visiteurs simultanés). Pas urgent tant qu'un seul visiteur teste à la fois.
- **Export PDF** : génération déjà en place (`pdf_export.py`) — bibliothèque à conserver telle quelle, aucun besoin identifié de la changer.
- **Frontend** : templates Django server-side (pas de framework JS lourd identifié dans le code actuel).

---

# Ajouts techniques nécessaires, module par module

## Authentification et rôles

- `django.contrib.auth` (déjà fourni par Django, pas encore branché sur les vues actuelles — à vérifier/activer).
- Modèle `Profil` (Partie 3) pour porter les rôles.
- Décorateurs `@login_required` et vérification de rôle sur les vues sensibles (validation de visite, administration).

## Upload de photos

- `Pillow` (dépendance standard Django pour `ImageField`) — à ajouter à `requirements.txt` si absent.
- Stockage local (`MEDIA_ROOT`) suffisant tant que le volume reste raisonnable ; migration vers un stockage objet (S3 ou équivalent) **seulement si le volume de photos le justifie** — non prioritaire.

## Coordonnées GPS

- Simples `DecimalField` (latitude, longitude) — pas besoin d'une extension géospatiale (PostGIS) pour un simple stockage de coordonnées sans requêtes géospatiales complexes. À réévaluer seulement si un besoin de recherche « établissements dans un rayon de X km » apparaît.

## Cartographie interactive (Phase 4 du plan reçu — vision, pas immédiate)

- Le plan reçu mentionne Leaflet/OpenLayers et des plans SVG interactifs. **Décision pour ce cahier des charges** : ce besoin correspond à une cartographie géographique (carte du monde/pays) ou à un plan dessiné (SVG) d'un étage — deux choses différentes :
  - Pour situer un établissement sur une carte (à partir des coordonnées GPS) : Leaflet est effectivement l'outil adapté, léger, sans dépendance lourde.
  - Pour un plan d'étage interactif (chambres cliquables) : ce n'est pas une carte géographique, donc pas besoin de Leaflet — un simple SVG généré (positions calculées, pas dessinées à la main) suffit dans un premier temps, cohérent avec la Partie 6.
- **Ces deux briques ne sont pas nécessaires pour les Parties 1 à 4 du modèle de données** (Bâtiment/Étage/Service/Chambre/Lit) : un simple export en listes/grilles (déjà le mode actuel de `cartographie.html`) fonctionne sans ajout technique. La brique cartographique visuelle est donc reportée à une étape ultérieure du plan de développement (Partie 7), pas un prérequis.

## Export JSON vers le SIH

- Déjà en grande partie couvert par DRF (sérialiseurs existants, `serializers.py`) — extension plutôt que nouvel outil.

---

# Environnements

- **Développement** : SQLite, `DEBUG=True`, tel qu'actuellement.
- **Production (quand ce sera nécessaire)** : PostgreSQL, `DEBUG=False`, variables d'environnement pour les secrets (`SECRET_KEY`, identifiants base de données) — actuellement à vérifier si en dur dans `settings.py`, à corriger avant toute mise en ligne réelle.

---

# Ce qui n'est pas retenu dans ce cahier des charges

- **Framework JS lourd (React, Vue)** : aucun besoin identifié qui justifie de sortir des templates Django server-side. Le plan d'écrans (Partie 6) reste compatible avec des templates classiques, éventuellement un peu de JS ciblé (déjà le cas dans `cartographie.html` pour les interactions dynamiques).
- **Microservices / architecture distribuée** : config reste une application Django monolithique. Rien dans les besoins fonctionnels ne justifie une complexité d'architecture distribuée à ce stade.
- **PostGIS** : voir ci-dessus, non retenu tant qu'aucune requête géospatiale complexe n'est nécessaire.

---
---

# PARTIE 6
# UX / UI
## config — Dossier de Conception

---

# Introduction

Cette partie décrit les écrans principaux, dans la continuité du parcours utilisateur (Partie 4). Elle ne fixe pas de maquette graphique pixel-perfect (hors périmètre d'un dossier texte), mais la structure, le contenu et le comportement de chaque écran.

---

# Principes transversaux

- **Un écran, une action principale.** Chaque écran a un objectif clair ; les actions secondaires restent visibles mais discrètes.
- **Le niveau de détail ne s'impose jamais.** Chaque écran de la cartographie propose le mode rapide en premier, le mode détaillé en option (jamais l'inverse).
- **Rien ne doit être ressaisi.** Toute information déjà connue (établissement, étage parent...) est pré-remplie dans les formulaires suivants.

---

# Écran — Tableau de bord

**Mis à jour à partir de la maquette (écran 1).** Zones de l'écran :

- En-tête personnalisé (« Bonjour, Marie ») + bouton « Nouvelle visite » (action principale) + notifications.
- Quatre indicateurs chiffrés en tête : Établissements (total recensés), Visites (total), En cours, Rapports générés.
- Tableau « Visites récentes » : établissement, date, statut, barre de progression — reprend l'avancement défini en Partie 3/4.
- Bloc « Visites par statut » : anneau de répartition (En cours / Terminées / Brouillon).
- Bloc « Progression globale » : pourcentage moyen d'avancement toutes visites confondues, avec mini-graphique de tendance.

La maquette confirme et enrichit ce qui était prévu (Partie 4, Étape 2) sans le contredire.

---

# Écran — Liste des établissements

- Barre de recherche (nom, ville).
- Filtres : région, type d'établissement.
- Liste ou grille de cartes, chacune avec : nom, ville, nombre de visites effectuées, date de dernière visite.
- Bouton « Nouvel établissement ».

---

# Écran — Détail d'un établissement

- En-tête : nom, type, contact, carte de localisation (si coordonnées GPS renseignées — Leaflet, Partie 5).
- Photo de façade si disponible.
- Liste des visites de cet établissement, triées par date, avec leur statut.
- Bouton « Nouvelle visite pour cet établissement ».

---

# Écran — Détail d'une visite

L'écran central du parcours (Étape 5 à 8 de la Partie 4). Structure proposée :

- **Bandeau supérieur** : établissement, date, statut (avec les couleurs suivantes, cohérentes avec le vocabulaire déjà utilisé en cartographie : gris = Brouillon, bleu = En cours, orange = Terminé en attente de validation, vert = Validé).
- **Barre d'avancement** : pourcentage global + liste des 5 sections avec coche si remplie.
- **Onglets ou accordéon** pour les 5 sections du questionnaire (Identification, Cartographie, IT, Effectifs, Processus/priorités) — accordéon recommandé pour rester sur un seul écran sans navigation, cohérent avec « pas de tunnel obligatoire » (Partie 4).
- **Bloc cartographie** : résumé chiffré (nb bâtiments, services, chambres, lits recensés) + lien vers l'écran cartographie détaillé.
- **Bloc photos** : galerie miniature + ajout rapide.
- **Actions** : Dupliquer, Exporter PDF, Marquer Terminé, (si Responsable) Valider.

---

# Écran — Cartographie

Évolution de `cartographie.html` existant. Deux modes d'affichage, sélectionnables par l'utilisateur :

## Mode liste (existant, conservé)

Le mode actuel — accordéon Zone → Chambre → Lit. **Reste le mode par défaut** : c'est le plus rapide à utiliser sur le terrain, y compris sur mobile/tablette.

## Mode plan (nouveau, Phase 4 du plan reçu)

**Mis à jour à partir de la maquette (écrans 5 et 6) — plus riche que la première version de cette partie.** Deux sous-écrans :

### Vue des bâtiments (écran 5)

- Carte du site avec les bâtiments positionnés (vue Plan ou Satellite, sélectionnable — cohérent avec l'usage de Leaflet posé en Partie 5 pour situer un établissement).
- Calques activables : Bâtiments, Services, Équipements, Photos — chaque calque superpose ses propres marqueurs sur la carte.
- Chaque bâtiment est une forme colorée cliquable, avec légende (Bâtiment A – Urgences, Bâtiment B – Bloc opératoire...).

### Plan d'un étage (écran 6)

- Sélecteurs Bâtiment → Étage en haut.
- Plan en grille des chambres/services de l'étage, avec couloirs et zones communes représentés.
- **Couleur de chaque chambre selon le niveau de recensement**, pas un statut d'occupation temps réel (confirmation du principe posé en Partie 1 — config n'est pas un outil temps réel) : Complète (vert) / Partielle (jaune) / Estimation (orange) / Non visitée (gris) / Anomalie (rouge). La légende est affichée en permanence dans le panneau latéral.
- Clic sur une chambre → panneau latéral avec infos rapides (type, lits, statut) et lien « Voir le détail » vers l'écran Détail d'une chambre.
- Bouton « Ajouter une chambre » directement sur ce plan (cohérent avec Partie 2 : chaque niveau se crée depuis la visite, sans écran séparé).

**Ce mode plan reste secondaire et non bloquant** : un visiteur pressé n'a jamais besoin d'y toucher pour compléter sa visite (mode liste toujours disponible en alternative).

---

# Écran — Détail d'une chambre (panneau ou modal)

- Numéro, capacité prévue, notes.
- Liste des lits, chacun avec son statut fonctionnel/non fonctionnel et ses équipements (texte libre + fiches détaillées si saisies).
- Bouton d'ajout rapide de lit.
- Galerie photo de la chambre.

---

# Écran — Rapport (aperçu avant export PDF)

- Non prioritaire comme écran séparé (Partie 2) : dans un premier temps, l'aperçu se fait en ouvrant directement le PDF généré. Un écran de prévisualisation en ligne est une amélioration possible, pas un prérequis.

---

# Écran — Administration

- Liste des utilisateurs avec leur rôle, activable/désactivable.
- Listes de choix paramétrables (types d'établissement, types d'équipement) — via le Django Admin existant dans un premier temps (Partie 2), avant de justifier une interface sur mesure.
- Journal d'activité, filtrable par utilisateur et par type d'action.

---

# Responsive

Cohérent avec l'usage terrain identifié en Partie 1 (le visiteur est en déplacement) :

- **Mobile / tablette** : mode liste privilégié partout, formulaires en une colonne, boutons larges.
- **Desktop** : mode plan de la cartographie disponible en plus, écrans multi-colonnes (ex. tableau de bord).

---
---

# PARTIE 7
# Plan de Développement
## config — Dossier de Conception

---

# Introduction

Cette dernière partie ordonne tout ce qui précède en étapes de développement concrètes, dans un ordre qui évite les refontes : chaque étape s'appuie sur la précédente sans obliger à revenir en arrière.

---

# Ordre de développement proposé

## Étape 1 — Statuts et avancement de visite

- Extension `StatutVisite` (ajout `en_cours`).
- Propriété `avancement` calculée sur `Visite`.
- Mise à jour des templates concernés.

*Pourquoi en premier* : c'est le changement le plus isolé, sans nouvelle table, qui apporte une valeur immédiate au parcours (Partie 4, Étapes 5 et 8).

## Étape 2 — Authentification et rôles

- Activation de `django.contrib.auth` sur les vues.
- Modèle `Profil` + rôles.
- `Visite.cree_par`.

*Pourquoi ensuite* : nécessaire avant d'introduire la validation par un Responsable de mission (étape suivante), et avant l'Administration.

## Étape 3 — Validation de visite et journal d'activité

- Statut `Validé` distinct, restriction d'accès par rôle.
- Modèle `JournalActivite`, écriture aux points clés.

## Étape 4 — Établissement : GPS et photo de façade

- Champs `latitude`/`longitude`.
- Modèle `Photo` (créé ici, réutilisé ensuite pour chambres/équipements).

*Pourquoi ici* : introduit le modèle `Photo` sur le cas le plus simple (une photo, un établissement) avant de l'étendre à des rattachements multiples.

## Étape 5 — Hiérarchie Bâtiment / Étage

- Modèles `Batiment`, `Etage`.
- `Zone.etage_obj` (FK nullable), renommage `etage` → `etage_libre`.
- Écrans de création intégrés à la cartographie (mode liste d'abord, cohérent avec Partie 6).

*Pourquoi seulement maintenant* : c'est le changement de modèle le plus délicat (Partie 3) — mieux vaut l'aborder une fois l'authentification et les rôles en place, pour pouvoir tester les permissions de création en même temps.

## Étape 6 — Équipements

- Modèle `Equipement`.
- Intégration à l'écran chambre (Partie 6).

## Étape 7 — Photos étendues

- Rattachement `Photo` aux chambres et équipements (le modèle existe depuis l'étape 4, on étend son usage).
- Galerie dans l'écran de détail de visite.

## Étape 8 — Mode plan de la cartographie

- Écran « Mode plan » (Partie 6), grille de cartes par étage.
- Reste additif : le mode liste existant n'est pas retiré.

## Étape 9 — Rapport enrichi

- Résumé, statistiques, anomalies, recommandations, galerie photo dans le PDF (Partie 2, module Rapports).

## Étape 10 — Administration

- Écran de gestion des utilisateurs et rôles (au-delà du Django Admin déjà utilisable dès l'étape 2).
- Listes de choix paramétrables.

## Étape 11 — Export JSON vers le SIH *(conditionnelle)*

- **Ne démarre pas automatiquement après l'étape 10.** Cette étape est déclenchée seulement quand `vision-et-etapes.md` — étape A côté HealthTracker (modèle Chambre/Lit) — devient réelle. Tant que ce n'est pas le cas, il n'y a personne pour consommer cet export.

---

# Ce que ce plan garantit

- Chaque étape est déployable et utile seule (aucune étape ne laisse l'application dans un état intermédiaire cassé).
- Aucune étape ne dépend d'une étape plus tardive — pas de dépendance circulaire.
- Le mode rapide existant (estimation, texte libre) n'est jamais retiré : chaque étape est additive, conformément au principe de gradation posé dès la Partie 1.

---

# Clôture du dossier

Ce dossier de conception, en sept parties, part de la vision (Partie 1) jusqu'au plan de développement (Partie 7), en passant par l'architecture fonctionnelle, le modèle de données, le parcours utilisateur, le cahier des charges technique et l'UX/UI.

Il vient s'ajouter à ce qui existe déjà et fonctionne (Partie 1) — rien dans ce dossier ne remet en cause le code actuel d'config, qui reste utilisable pendant toute la durée de sa mise en œuvre.

---
---

# PARTIE 8
# Sécurité
## config — Dossier de Conception

---

# Introduction

Cette partie fixe le niveau de sécurité d'config. Principe directeur : **une sécurité proportionnée à la sensibilité réelle des données**, pas un maximalisme qui ralentirait le développement sans bénéfice concret.

Point de cadrage important, à garder en tête pour toute cette partie : **config ne contient aucune donnée médicale ou patient**. Ce n'est pas un logiciel de santé au sens réglementaire — c'est HealthTracker qui portera cette responsabilité le moment venu. config manipule des données d'infrastructure, de contact professionnel, et de recensement physique. Cela oriente tout ce qui suit : pas de chiffrement de niveau "dossier médical", mais une vraie rigueur sur les points qui comptent.

---

# Les trois niveaux de sensibilité identifiés

## Niveau 1 — Critique : les identifiants d'infrastructure

Le module Infrastructure IT (Partie 2) peut amener un visiteur à noter, pendant un audit, des informations comme un mot de passe Wi-Fi ou un accès à un équipement réseau.

**Décision** : le champ correspondant doit être conçu pour **ne jamais stocker un secret en clair de façon durable et consultable**. Deux options possibles, à trancher techniquement en Partie 7 (développement) :

- Ne pas prévoir de champ dédié « mot de passe » du tout — le questionnaire IT actuel ne le demande pas explicitement (à vérifier dans les champs existants), et ce choix doit rester ainsi.
- Si un tel besoin apparaît malgré tout (ex. accès temporaire à documenter pour la mission), le champ doit être chiffré en base (chiffrement applicatif, pas juste "protégé par les permissions"), avec accès restreint au strict rôle Responsable de mission.

## Niveau 2 — Sensible : les données personnelles de contact

Noms, téléphones, emails des contacts établissement, et des comptes utilisateurs config eux-mêmes.

**Décision** : protection standard, pas de chiffrement spécifique nécessaire au-delà de ce qu'apporte une base de données correctement sécurisée (accès réseau restreint, sauvegardes chiffrées — voir plus bas). C'est le niveau de rigueur qu'on appliquerait à n'importe quelle application professionnelle sérieuse.

## Niveau 3 — Modéré : la cartographie physique et les photos

Plans, équipements, photos de locaux. Sensible surtout en cas de fuite massive (cartographie de sécurité d'un établissement), mais pas une donnée réglementée.

**Décision** : protégé par les permissions par rôle déjà prévues (Partie 2/3), sans mesure technique supplémentaire.

---

# Mesures de sécurité retenues

## Authentification

- Mots de passe : jamais stockés en clair — Django le fait déjà correctement par défaut (hashage PBKDF2/Argon2), à ne surtout pas modifier ou "simplifier".
- Politique de mot de passe minimale : longueur, pas de mot de passe trivial (validateurs Django standards, déjà disponibles, à activer si pas déjà fait).
- **Authentification à deux facteurs (2FA)** : recommandée pour les comptes Responsable de mission et Administrateur (accès aux données les plus larges), optionnelle pour les Visiteurs. Pas un chantier lourd — une bibliothèque standard Django (`django-otp` ou équivalent) suffit.
- Verrouillage temporaire après plusieurs échecs de connexion (protection anti-brute-force basique).

## Transport et infrastructure

- **HTTPS obligatoire** en production, sans exception — non négociable, quel que soit le niveau de sensibilité des données, car c'est la base qui protège les mots de passe de connexion eux-mêmes en transit.
- Secrets d'application (`SECRET_KEY`, identifiants base de données) en variables d'environnement, jamais en dur dans `settings.py` (point déjà soulevé en Partie 5, confirmé ici comme exigence de sécurité, pas seulement de bonne pratique).
- Sauvegardes de la base de données chiffrées au repos.

## Permissions et traçabilité

- Le système de rôles (Visiteur / Responsable de mission / Administrateur, Partie 2/3) reste le mécanisme principal de protection des données : chacun ne voit que ce qui est nécessaire à son rôle.
- Le `JournalActivite` (Partie 3) sert aussi de mesure de sécurité : toute action sensible (validation, suppression, export) est tracée avec qui, quoi, quand.

## Ce qui est volontairement laissé de côté pour l'instant

- **Chiffrement de bout en bout** : non retenu — pertinent pour une messagerie privée, pas pour une application métier où le serveur doit de toute façon pouvoir lire les données pour générer rapports et exports.
- **Audit de sécurité externe / pentest** : à prévoir avant un déploiement en production à grande échelle, pas nécessaire pendant le développement.
- **Conformité réglementaire type HDS (Hébergeur de Données de Santé)** : **non applicable à config**, puisqu'il ne contient pas de données de santé. Ce sera un sujet pour HealthTracker le moment venu, pas pour config.

---

# Ce que ça change pour le plan de développement (Partie 7)

Une **Étape 2bis — Durcissement sécurité** est ajoutée juste après l'Étape 2 (Authentification et rôles) du plan de développement :

- Activation HTTPS et configuration des secrets en environnement.
- Validateurs de mot de passe Django.
- 2FA pour les rôles Responsable de mission et Administrateur.
- Verrouillage anti-brute-force.

Elle est positionnée tôt (juste après l'authentification de base) car chaque étape suivante du développement s'appuie sur des comptes utilisateurs — autant que ces comptes soient bien protégés dès le départ, plutôt que d'ajouter la sécurité après coup sur une base d'utilisateurs déjà créée.

---

**Fin de la Partie 8 – Sécurité**

**Fin du dossier de conception — config.**
