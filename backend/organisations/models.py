from django.db import models


class StatutEtablissement(models.TextChoices):
    ACTIF = 'actif', 'Actif'
    INACTIF = 'inactif', 'Inactif'
    FERME = 'ferme', 'Fermé'


class Etablissement(models.Model):
    TYPE_CHOICES = [
        ('hopital', 'Hôpital'),
        ('clinique', 'Clinique'),
        ('centre_sante', 'Centre de santé'),
        ('poste_sante', 'Poste de santé'),
        ('laboratoire', 'Laboratoire'),
        ('autre', 'Autre'),
    ]
    STATUT_JURIDIQUE_CHOICES = [
        ('public', 'Public'),
        ('prive', 'Privé'),
        ('confessionnel', 'Confessionnel'),
        ('ong', 'ONG'),
    ]

    nom = models.CharField(max_length=200)
    type = models.CharField(max_length=30, choices=TYPE_CHOICES)
    statut = models.CharField(max_length=10, choices=StatutEtablissement.choices, default=StatutEtablissement.ACTIF)
    statut_juridique = models.CharField(max_length=30, choices=STATUT_JURIDIQUE_CHOICES, blank=True)
    ville = models.CharField(max_length=100, blank=True)
    region = models.CharField(max_length=100, blank=True)
    adresse = models.CharField(max_length=255, blank=True)

    contact_nom = models.CharField(max_length=150, blank=True)
    contact_fonction = models.CharField(max_length=150, blank=True)
    contact_telephone = models.CharField(max_length=30, blank=True)
    contact_email = models.EmailField(blank=True)

    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['nom']

    def __str__(self):
        return self.nom

    @property
    def derniere_visite(self):
        # self.visites : relation inverse générée par missions.Visite.etablissement
        # (related_name='visites') — aucun import nécessaire, câblé par Django au
        # démarrage via le registre des apps, pas au niveau Python.
        return self.visites.order_by('-date_visite').first()

    # --- Compteurs "Résumé" (écran 4) ---
    # Imports différés (à l'intérieur des méthodes, pas en haut du fichier) : organizations
    # n'a besoin de connaître cartography/inventory qu'au moment d'exécuter ces requêtes,
    # jamais au chargement du module. Ça évite tout risque d'import circulaire avec les
    # autres apps, quel que soit l'ordre de chargement.

    @property
    def nb_batiments(self):
        return self.batiments.count()

    @property
    def nb_etages(self):
        from cartographie.models import Etage
        return Etage.objects.filter(batiment__etablissement=self).count()

    @property
    def nb_services(self):
        return self.zones.count()

    @property
    def nb_chambres(self):
        from cartographie.models import Chambre
        return Chambre.objects.filter(zone__etablissement=self).count()

    @property
    def nb_lits(self):
        from cartographie.models import Lit
        return Lit.objects.filter(chambre__zone__etablissement=self).count()

    @property
    def nb_equipements(self):
        from inventaire.models import Equipement
        return Equipement.objects.filter(
            models.Q(lit__chambre__zone__etablissement=self)
            | models.Q(chambre__zone__etablissement=self)
            | models.Q(zone__etablissement=self)
        ).distinct().count()
