from django.conf import settings
from django.db import models

from comptes.choices import EtatLocaux


class StatutVisite(models.TextChoices):
    BROUILLON = 'brouillon', 'Brouillon'
    EN_COURS = 'en_cours', 'En cours'
    TERMINE = 'termine', 'Terminé'
    ENVOYE = 'envoye', 'Validé'  # libellé renommé, valeur technique conservée (Partie 3)


class TypeVisite(models.TextChoices):
    """Distingue le recensement initial d'un contrôle de suivi — pas un nouveau
    rôle utilisateur, juste une nature de visite (même personne, même permissions,
    portée différente : un contrôle de suivi ne remappe pas tout, il vérifie
    l'état de ce qui existe déjà)."""
    INITIALE = 'initiale', 'Recensement initial'
    SUIVI = 'suivi', 'Contrôle de suivi'


class Visite(models.Model):
    # Import direct de apps.organizations.models : organizations ne dépend jamais
    # de missions (vérifié — Etablissement n'importe rien de missions au niveau
    # module), donc aucun risque de cycle dans ce sens précis.
    etablissement = models.ForeignKey('organisations.Etablissement', on_delete=models.CASCADE, related_name='visites')
    auteur = models.CharField(max_length=150, blank=True)  # conservé pour compat
    cree_par = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='visites_creees',
    )
    date_visite = models.DateField()
    statut = models.CharField(max_length=15, choices=StatutVisite.choices, default=StatutVisite.BROUILLON)
    type_visite = models.CharField(max_length=10, choices=TypeVisite.choices, default=TypeVisite.INITIALE)

    possede_urgences = models.BooleanField(default=False)
    bloc_operatoire = models.BooleanField(default=False)
    laboratoire = models.BooleanField(default=False)
    pharmacie = models.BooleanField(default=False)
    imagerie = models.BooleanField(default=False)

    etat_locaux = models.CharField(max_length=15, choices=EtatLocaux.choices, blank=True)
    notes_libres = models.TextField(blank=True)

    # --- Volet Infrastructure IT ---
    reseau_disponible = models.BooleanField(default=False)
    wifi_disponible = models.BooleanField(default=False)
    couverture_wifi = models.CharField(max_length=255, blank=True)
    nb_postes_informatiques = models.PositiveIntegerField(null=True, blank=True)
    observations_it = models.TextField(blank=True)

    # --- Volet Effectifs ---
    effectif_medecins = models.PositiveIntegerField(null=True, blank=True)
    effectif_infirmiers = models.PositiveIntegerField(null=True, blank=True)
    effectif_autres = models.PositiveIntegerField(null=True, blank=True)

    # --- Volet Processus / Priorités ---
    processus_actuels = models.TextField(blank=True)
    priorites_contraintes = models.TextField(blank=True)

    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_visite']

    def __str__(self):
        return f"Visite {self.etablissement.nom} — {self.date_visite}"

    # --- Compteurs : ce que CETTE visite a créé/mis à jour (derniere_visite_maj),
    # pas l'état global de l'établissement. Imports différés vers cartography
    # (cartography ne dépend jamais de missions au niveau module — les FK y sont
    # en string 'missions.Visite' — donc missions PEUT importer cartography
    # directement sans créer de cycle. Je garde quand même l'import différé ici
    # par cohérence avec le reste du fichier et pour limiter le couplage au strict
    # nécessaire).

    @property
    def nb_batiments(self):
        from cartographie.models import Batiment
        return Batiment.objects.filter(derniere_visite_maj=self).count()

    @property
    def nb_zones(self):
        from cartographie.models import Zone
        return Zone.objects.filter(derniere_visite_maj=self).count()

    @property
    def nb_chambres(self):
        from cartographie.models import Chambre
        return Chambre.objects.filter(derniere_visite_maj=self).count()

    @property
    def nb_lits(self):
        from cartographie.models import Lit
        return Lit.objects.filter(chambre__derniere_visite_maj=self).count()

    @property
    def avancement(self):
        """Pourcentage de sections remplies (calculé, pas stocké — Partie 3)."""
        from cartographie.models import Zone

        sections = [
            bool(self.etat_locaux),
            Zone.objects.filter(etablissement=self.etablissement).exists(),
            self.reseau_disponible or self.wifi_disponible or bool(self.observations_it),
            any([self.effectif_medecins, self.effectif_infirmiers, self.effectif_autres]),
            bool(self.processus_actuels) or bool(self.priorites_contraintes),
            ]
        remplies = sum(1 for s in sections if s)
        return round(remplies / len(sections) * 100)


class MembreEquipe(models.Model):
    visite = models.ForeignKey(Visite, on_delete=models.CASCADE, related_name='membres_equipe')
    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    est_inspecteur_principal = models.BooleanField(default=False)

    class Meta:
        unique_together = ('visite', 'utilisateur')
        ordering = ['id']

    def __str__(self):
        return f"{self.utilisateur} sur {self.visite}"


class Commentaire(models.Model):
    visite = models.ForeignKey(Visite, on_delete=models.CASCADE, related_name='commentaires')
    auteur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    texte = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_creation']

    def __str__(self):
        return f"Commentaire de {self.auteur} sur {self.visite}"
