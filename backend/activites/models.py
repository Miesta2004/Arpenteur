from django.conf import settings
from django.db import models


class JournalActivite(models.Model):
    """Traçabilité minimale (Partie 8)"""
    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=50)  # ex. "creation", "modification", "validation"
    objet_type = models.CharField(max_length=50)  # ex. "Visite", "Batiment"
    objet_id = models.PositiveIntegerField()
    description = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']
        verbose_name = "Entrée du journal d'activité"
        verbose_name_plural = "Journal d'activité"

    def __str__(self):
        return f"[{self.date:%Y-%m-%d %H:%M}] {self.action} — {self.objet_type} #{self.objet_id}"
