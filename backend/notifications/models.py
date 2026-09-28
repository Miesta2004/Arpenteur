import secrets

from django.db import models


class WebhookEndpoint(models.Model):
    """Un système externe (HealthTracker) enregistre ici l'URL où il veut recevoir
    les notifications de changement, et les types d'événements qui l'intéressent."""

    nom = models.CharField(max_length=150, help_text="Ex. 'HealthTracker — environnement production'")
    url = models.URLField()
    secret = models.CharField(
        max_length=64, blank=True,
        help_text="Généré automatiquement — sert à signer les envois (HMAC) pour que le "
                  "destinataire vérifie que la requête vient bien d'Arpenteur.",
    )
    evenements_abonnes = models.JSONField(
        default=list,
        help_text="Liste des types d'événements écoutés, ex. [\"Lit\", \"Equipement\"]. "
                  "Liste vide = tous les événements.",
    )
    actif = models.BooleanField(default=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['nom']

    def save(self, *args, **kwargs):
        if not self.secret:
            self.secret = secrets.token_hex(32)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom

    def interesse_par(self, type_objet):
        return not self.evenements_abonnes or type_objet in self.evenements_abonnes


class StatutEnvoi(models.TextChoices):
    EN_ATTENTE = 'en_attente', 'En attente'
    ENVOYE = 'envoye', 'Envoyé'
    ECHEC = 'echec', 'Échec'


class EvenementSync(models.Model):
    """File d'événements (pattern outbox) : chaque changement structurel pertinent
    (Lit, Chambre, Equipement...) crée une entrée ici via un signal (voir
    notifications/signals.py). Une tâche Celery (voir tasks.py) les envoie ensuite
    aux webhooks abonnés, avec réessai en cas d'échec — ni Arpenteur ni
    HealthTracker n'ont besoin d'être en ligne au même instant pour que ça marche."""

    type_objet = models.CharField(max_length=50)  # ex. "Lit", "Chambre", "Equipement"
    objet_id = models.PositiveIntegerField()
    action = models.CharField(max_length=15)  # "creation", "modification", "suppression"
    payload = models.JSONField(help_text="Instantané des données pertinentes au moment de l'événement")

    statut_envoi = models.CharField(max_length=12, choices=StatutEnvoi.choices, default=StatutEnvoi.EN_ATTENTE)
    tentatives = models.PositiveIntegerField(default=0)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_dernier_essai = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-date_creation']

    def __str__(self):
        return f"{self.action} {self.type_objet} #{self.objet_id} — {self.get_statut_envoi_display()}"
