from rest_framework import permissions
from .capacites import Capacite


def get_role(user):
    """Récupère le rôle de l'utilisateur via son profil."""
    if not user or not user.is_authenticated:
        return None
    if user.is_superuser:
        return 'admin'
    profil = getattr(user, 'profil', None)
    return profil.role if profil else None


class EstResponsableOuAdmin(permissions.BasePermission):
    """Réservé aux actions de supervision : validation, export, administration."""

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True

        # VALIDATION_MISSIONS (pas ADMINISTRATION_SERVICE) : c'est la capacité
        # accordée aux responsables ET aux admins d'après capacites.py. Utiliser
        # ADMINISTRATION_SERVICE ici excluait les responsables (accordée aux
        # admins seuls), contredisant le nom de cette permission et la Partie 2
        # du dossier ("Responsable de mission : validation des visites").
        return Capacite.has_capacity(request.user, Capacite.VALIDATION_MISSIONS)


class EstAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return get_role(request.user) == 'admin' or (request.user and request.user.is_superuser)