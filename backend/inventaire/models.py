from django.core.exceptions import ValidationError
from django.db import models

from cartographie.models import Chambre, Lit, Zone


class EtatEquipement(models.TextChoices):
    FONCTIONNEL = 'fonctionnel', 'Fonctionnel'
    EN_PANNE = 'en_panne', 'En panne'
    A_VERIFIER = 'a_verifier', 'À vérifier'


class CategorieEquipement(models.TextChoices):
    MEDICAL = 'medical', 'Médical'
    INFORMATIQUE = 'informatique', 'Informatique'
    MOBILIER = 'mobilier', 'Mobilier'
    AUTRE = 'autre', 'Autre'


class DisponibiliteEquipement(models.TextChoices):
    """Même logique que EtatLit : constaté à la dernière visite, pas suivi live —
    "en_utilisation" ne veut pas dire "rattaché à un patient précis", juste
    "occupé par un usage en cours au moment du constat"."""
    DISPONIBLE = 'disponible', 'Disponible'
    EN_UTILISATION = 'en_utilisation', 'En utilisation'
    RESERVE = 'reserve', 'Réservé'
    INDISPONIBLE = 'indisponible', 'Indisponible'


class Equipement(models.Model):
    # Ici, import direct de apps.cartographie.models (pas de string ref) : cartographie
    # ne dépend jamais d'inventory (vérifié), donc aucun risque de cycle dans ce sens.
    lit = models.ForeignKey(Lit, on_delete=models.CASCADE, null=True, blank=True, related_name='equipements_lies')
    chambre = models.ForeignKey(Chambre, on_delete=models.CASCADE, null=True, blank=True, related_name='equipements_lies')
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE, null=True, blank=True, related_name='equipements_lies')

    nom = models.CharField(max_length=150)
    categorie = models.CharField(max_length=15, choices=CategorieEquipement.choices, default=CategorieEquipement.MEDICAL)
    numero_inventaire = models.CharField(max_length=50, blank=True)
    etat = models.CharField(max_length=15, choices=EtatEquipement.choices, default=EtatEquipement.FONCTIONNEL)
    disponibilite = models.CharField(
        max_length=15, choices=DisponibiliteEquipement.choices, default=DisponibiliteEquipement.DISPONIBLE
    )
    fabricant = models.CharField(max_length=100, blank=True)
    annee = models.PositiveIntegerField(null=True, blank=True)
    observations = models.TextField(blank=True)

    class Meta:
        ordering = ['nom']

    def __str__(self):
        return self.nom

    def clean(self):
        # Contrainte applicative, pas SQL (Partie 3, §8) : au moins un rattachement.
        # Vérifiée par le serializer à l'écriture, pas par clean() directement (voir
        # EquipementSerializer.validate) — pour ne pas casser un futur import externe imparfait.
        if not any([self.lit_id, self.chambre_id, self.zone_id]):
            raise ValidationError("Un équipement doit être rattaché à un lit, une chambre ou un service.")


class TypeIntervention(models.TextChoices):
    PREVENTIVE = 'preventive', 'Préventive'
    CORRECTIVE = 'corrective', 'Corrective'


class MaintenanceEquipement(models.Model):
    """Historique des interventions — plutôt que deux champs de date sur
    Equipement, garde une trace de chaque passage (cohérent avec la logique de
    traçabilité déjà en place ailleurs dans le projet, Partie 8)."""
    equipement = models.ForeignKey(Equipement, on_delete=models.CASCADE, related_name='interventions')
    type_intervention = models.CharField(max_length=12, choices=TypeIntervention.choices)
    date = models.DateField()
    technicien = models.CharField(max_length=150, blank=True)
    description = models.TextField(blank=True)
    prochain_controle = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.get_type_intervention_display()} — {self.equipement.nom} ({self.date})"


class Photo(models.Model):
    image = models.ImageField(upload_to='photos/%Y/%m/')
    legende = models.CharField(max_length=255)  # obligatoire — une photo doit avoir un sens hors contexte

    # FK cross-app en string : organisations et missions n'ont pas besoin d'être
    # importés ici, évite tout couplage supplémentaire.
    etablissement = models.ForeignKey('organisations.Etablissement', on_delete=models.CASCADE, null=True, blank=True, related_name='photos')
    visite = models.ForeignKey('missions.Visite', on_delete=models.CASCADE, null=True, blank=True, related_name='photos')
    chambre = models.ForeignKey(Chambre, on_delete=models.CASCADE, null=True, blank=True, related_name='photos')
    equipement = models.ForeignKey(Equipement, on_delete=models.CASCADE, null=True, blank=True, related_name='photos')

    date_ajout = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_ajout']

    def __str__(self):
        return self.legende
