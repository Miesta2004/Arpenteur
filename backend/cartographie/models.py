from django.db import models

from comptes.choices import EtatLocaux


class TypePiece(models.TextChoices):
    """Nature générale de la pièce — s'applique à TOUTE pièce du bâtiment, pas
    seulement les chambres patient. Indépendant de categorie_chambre/specialite/
    niveau_confort sur Chambre, qui n'affinent que le cas où type_piece=CHAMBRE_PATIENT."""
    CHAMBRE_PATIENT = 'chambre_patient', 'Chambre patient'
    CONSULTATION = 'consultation', 'Salle de consultation'
    BUREAU_MEDECIN = 'bureau_medecin', 'Bureau médecin'
    OPERATION = 'operation', "Salle d'opération"
    ACCUEIL_ATTENTE = 'accueil_attente', "Accueil / Salle d'attente"
    TOILETTES = 'toilettes', 'Toilettes'
    STOCK = 'stock', 'Stock'
    TECHNIQUE_INFORMATIQUE = 'technique_informatique', 'Salle technique / informatique'
    AUTRE = 'autre', 'Autre'


class CategorieChambre(models.TextChoices):
    """Classe d'occupation/intimité — indépendant de la spécialité clinique et
    du niveau de confort (une chambre peut être Individuelle + Réanimation + VIP
    en même temps, d'où 3 champs séparés plutôt qu'un seul "type de chambre")."""
    COMMUNE = 'commune', 'Commune'
    DOUBLE = 'double', 'Double'
    INDIVIDUELLE = 'individuelle', 'Individuelle'
    SUITE = 'suite', 'Suite'


class SpecialiteChambre(models.TextChoices):
    GENERALE = 'generale', 'Générale'
    ISOLEMENT = 'isolement', 'Isolement'
    REANIMATION = 'reanimation', 'Réanimation'
    SOINS_INTENSIFS = 'soins_intensifs', 'Soins intensifs'
    MATERNITE = 'maternite', 'Maternité'
    PEDIATRIE = 'pediatrie', 'Pédiatrie'
    PSYCHIATRIE = 'psychiatrie', 'Psychiatrie'


class NiveauConfort(models.TextChoices):
    STANDARD = 'standard', 'Standard'
    CONFORT = 'confort', 'Confort'
    PREMIUM = 'premium', 'Premium'
    VIP = 'vip', 'VIP'


class EtatLit(models.TextChoices):
    """Important : c'est l'état CONSTATÉ LORS DE LA DERNIÈRE VISITE d'audit, pas
    un suivi en temps réel de l'occupation patient (Arpenteur ne gère jamais les
    patients — voir derniere_visite_maj sur Lit, même principe que le reste du
    modèle). La gestion live de l'occupation (admission/sortie) reste le rôle de
    HealthTracker, qui consomme ces données via la synchronisation (app notifications)."""
    DISPONIBLE = 'disponible', 'Disponible'
    OCCUPE = 'occupe', 'Occupé'
    RESERVE = 'reserve', 'Réservé'
    EN_NETTOYAGE = 'en_nettoyage', 'En nettoyage'
    EN_MAINTENANCE = 'en_maintenance', 'En maintenance'
    HORS_SERVICE = 'hors_service', 'Hors service'


class Caracteristique(models.Model):
    """Table de référence extensible (pas des champs booléens fixes sur Chambre) :
    ajouter une caractéristique se fait depuis l'admin, sans migration."""
    code = models.SlugField(max_length=50, unique=True)
    label = models.CharField(max_length=100)
    categorie = models.CharField(
        max_length=30, blank=True,
        help_text="Regroupement libre pour l'affichage (ex. 'confort', 'medical', 'accessibilite')",
    )
    ordre = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['ordre', 'label']
        verbose_name = 'Caractéristique de chambre'
        verbose_name_plural = 'Caractéristiques de chambre'

    def __str__(self):
        return self.label


class Batiment(models.Model):
    etablissement = models.ForeignKey('organisations.Etablissement', on_delete=models.CASCADE, related_name='batiments')
    nom = models.CharField(max_length=150)
    usage_principal = models.CharField(max_length=150, blank=True)
    nb_etages_declare = models.PositiveIntegerField(null=True, blank=True)
    etat_general = models.CharField(max_length=15, choices=EtatLocaux.choices, blank=True)
    ordre = models.PositiveIntegerField(default=0)

    derniere_visite_maj = models.ForeignKey('missions.Visite', on_delete=models.SET_NULL, null=True, blank=True, related_name='+')

    class Meta:
        ordering = ['ordre', 'nom']

    def __str__(self):
        return self.nom


class Etage(models.Model):
    batiment = models.ForeignKey(Batiment, on_delete=models.CASCADE, related_name='etages')
    nom = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    ordre = models.PositiveIntegerField(default=0)

    derniere_visite_maj = models.ForeignKey('missions.Visite', on_delete=models.SET_NULL, null=True, blank=True, related_name='+')

    class Meta:
        ordering = ['ordre', 'nom']

    def __str__(self):
        return f"{self.nom} ({self.batiment.nom})"


class Zone(models.Model):
    etablissement = models.ForeignKey('organisations.Etablissement', on_delete=models.CASCADE, related_name='zones')
    etage_obj = models.ForeignKey(Etage, on_delete=models.SET_NULL, null=True, blank=True, related_name='zones')
    etage_libre = models.CharField(max_length=50, blank=True)  # mode rapide, texte libre

    nom = models.CharField(max_length=150, verbose_name='Nom du service')
    type = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    ordre = models.PositiveIntegerField(default=0)

    nb_chambres_estime = models.PositiveIntegerField(null=True, blank=True)
    nb_lits_estime = models.PositiveIntegerField(null=True, blank=True)
    taux_occupation_pct = models.PositiveIntegerField(null=True, blank=True)

    derniere_visite_maj = models.ForeignKey('missions.Visite', on_delete=models.SET_NULL, null=True, blank=True, related_name='+')

    class Meta:
        verbose_name = 'Service'
        verbose_name_plural = 'Services'
        ordering = ['ordre', 'nom']

    def __str__(self):
        return self.nom

    def save(self, *args, **kwargs):
        if self.etage_obj_id and not self.etablissement_id:
            self.etablissement = self.etage_obj.batiment.etablissement
        super().save(*args, **kwargs)

    @property
    def nb_chambres_detaillees(self):
        return self.chambres.count()

    @property
    def a_detail(self):
        return self.chambres.exists()


class Unite(models.Model):
    """Niveau optionnel entre Service et Chambre (même principe de gradation
    qu'Étage : utile pour subdiviser un grand service en pavillons/unités
    physiques distincts, pas obligatoire pour un petit établissement)."""
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE, related_name='unites')
    nom = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    ordre = models.PositiveIntegerField(default=0)

    derniere_visite_maj = models.ForeignKey('missions.Visite', on_delete=models.SET_NULL, null=True, blank=True, related_name='+')

    class Meta:
        ordering = ['ordre', 'nom']

    def __str__(self):
        return f"{self.nom} ({self.zone.nom})"


class Chambre(models.Model):
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE, related_name='chambres')
    # Optionnelle : une chambre peut être rattachée directement au service (mode
    # rapide) ou, si le service est subdivisé, à une Unité précise.
    unite = models.ForeignKey(Unite, on_delete=models.SET_NULL, null=True, blank=True, related_name='chambres')

    numero = models.CharField(max_length=30)
    type_piece = models.CharField(max_length=25, choices=TypePiece.choices, default=TypePiece.CHAMBRE_PATIENT)

    # --- Typage riche (obligatoire — Décision architecture HealthTracker) ---
    categorie_chambre = models.CharField(max_length=15, choices=CategorieChambre.choices, default=CategorieChambre.COMMUNE)
    specialite = models.CharField(max_length=20, choices=SpecialiteChambre.choices, default=SpecialiteChambre.GENERALE)
    niveau_confort = models.CharField(max_length=10, choices=NiveauConfort.choices, default=NiveauConfort.STANDARD)
    caracteristiques = models.ManyToManyField(Caracteristique, blank=True, related_name='chambres')

    avec_lits = models.BooleanField(
        default=True,
        help_text="Détermine si la section Lits s'affiche (désactivé pour un bureau, une salle d'attente...)",
    )
    capacite_prevue = models.PositiveIntegerField(null=True, blank=True)
    notes = models.CharField(max_length=255, blank=True)

    derniere_visite_maj = models.ForeignKey('missions.Visite', on_delete=models.SET_NULL, null=True, blank=True, related_name='+')

    class Meta:
        ordering = ['numero']

    def __str__(self):
        return f"{self.get_type_piece_display()} {self.numero}"


class Lit(models.Model):
    chambre = models.ForeignKey(Chambre, on_delete=models.CASCADE, related_name='lits')
    identifiant = models.CharField(max_length=10)

    # Remplace l'ancien booléen `fonctionnel` — état constaté à la dernière visite
    # (voir docstring EtatLit), pas un suivi live de l'occupation patient.
    etat = models.CharField(max_length=15, choices=EtatLit.choices, default=EtatLit.DISPONIBLE)
    equipements = models.CharField(max_length=255, blank=True)  # texte libre, conservé (mode rapide)

    derniere_visite_maj = models.ForeignKey('missions.Visite', on_delete=models.SET_NULL, null=True, blank=True, related_name='+')

    class Meta:
        ordering = ['identifiant']

    def __str__(self):
        return f"Lit {self.identifiant} ({self.chambre})"

    @property
    def est_utilisable(self):
        """Le lit est-il structurellement en état de servir (peu importe s'il est
        actuellement occupé/réservé) ? Utile pour distinguer "indisponible car
        occupé par un patient" (question de HealthTracker) de "indisponible car
        cassé" (question d'Arpenteur)."""
        return self.etat not in (EtatLit.EN_MAINTENANCE, EtatLit.HORS_SERVICE)
