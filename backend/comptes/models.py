from django.conf import settings
from django.db import models


class RoleUtilisateur(models.TextChoices):
    VISITEUR = 'visiteur', 'Visiteur'
    RESPONSABLE = 'responsable', 'Responsable de mission'
    ADMIN = 'admin', 'Administrateur'


class Profil(models.Model):
    """Étend django.contrib.auth.User avec un rôle métier, sans remplacer le
    système d'authentification standard de Django (Partie 3, §10 : évite de
    réinventer l'auth pour un bénéfice faible)."""

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profil')
    role = models.CharField(max_length=15, choices=RoleUtilisateur.choices, default=RoleUtilisateur.VISITEUR)

    def __str__(self):
        return f"{self.user} ({self.get_role_display()})"
