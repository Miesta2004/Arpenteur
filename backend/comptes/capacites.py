"""
Système de capacités pour la gestion granulaire des permissions.
Les capacités héritent des rôles : un administrateur a toutes les capacités,
un responsable a les capacités de responsable, etc.
"""
from enum import Enum


class Capacite(str, Enum):
    """
    Énumération des capacités disponibles dans le système.
    Chaque capacité représente une action ou un ensemble d'actions
    qu'un utilisateur peut être autorisé à effectuer.
    """
    # Capacités d'administration système
    ADMINISTRATION_SERVICE = 'administration_service'  # Gestion générale du service
    GESTION_UTILISATEURS = 'gestion_utilisateurs'      # Créer/modifier/supprimer des utilisateurs
    GESTION_ROLES = 'gestion_roles'                    # Assigner/modifier les rôles

    # Capacités de supervision
    VALIDATION_MISSIONS = 'validation_missions'         # Valider les missions/visites
    EXPORT_DONNEES = 'export_donnees'                  # Exporter les données
    CONSULTATION_RAPPORTS = 'consultation_rapports'    # Consulter les rapports

    # Capacités de gestion d'établissement
    GESTION_ETABLISSEMENTS = 'gestion_etablissements'  # Gérer les établissements
    GESTION_MISSIONS = 'gestion_missions'              # Créer/modifier les missions
    SAISIE_MISSION = 'saisie_mission'                  # Saisir les résultats de mission

    # Capacités de consultation
    CONSULTATION_ETABLISSEMENTS = 'consultation_etablissements'  # Consulter les établissements
    CONSULTATION_MISSIONS = 'consultation_missions'              # Consulter les missions

    @classmethod
    def get_capacities_for_role(cls, role):
        """
        Retourne les capacités associées à un rôle donné.

        Args:
            role (str): Le rôle de l'utilisateur ('admin', 'responsable', 'visiteur')

        Returns:
            set: Ensemble des capacités accessibles pour ce rôle
        """
        # Capacités par rôle avec héritage (admin > responsable > visiteur)
        role_capacities = {
            'admin': {
                cls.ADMINISTRATION_SERVICE,
                cls.GESTION_UTILISATEURS,
                cls.GESTION_ROLES,
                cls.VALIDATION_MISSIONS,
                cls.EXPORT_DONNEES,
                cls.CONSULTATION_RAPPORTS,
                cls.GESTION_ETABLISSEMENTS,
                cls.GESTION_MISSIONS,
                cls.SAISIE_MISSION,
                cls.CONSULTATION_ETABLISSEMENTS,
                cls.CONSULTATION_MISSIONS,
            },
            'responsable': {
                cls.VALIDATION_MISSIONS,
                cls.EXPORT_DONNEES,
                cls.CONSULTATION_RAPPORTS,
                cls.GESTION_ETABLISSEMENTS,
                cls.GESTION_MISSIONS,
                cls.SAISIE_MISSION,
                cls.CONSULTATION_ETABLISSEMENTS,
                cls.CONSULTATION_MISSIONS,
            },
            'visiteur': {
                cls.SAISIE_MISSION,
                cls.CONSULTATION_ETABLISSEMENTS,
                cls.CONSULTATION_MISSIONS,
            },
        }
        return role_capacities.get(role, set())

    @classmethod
    def has_capacity(cls, user, capacite):
        """
        Vérifie si un utilisateur possède une capacité donnée.

        Args:
            user: L'objet utilisateur Django
            capacite: La capacité à vérifier (instance de Capacite)

        Returns:
            bool: True si l'utilisateur possède la capacité, False sinon
        """
        if not user or not user.is_authenticated:
            return False

        # Les superutilisateurs ont toutes les capacités
        if user.is_superuser:
            return True

        # Récupère le profil utilisateur
        profil = getattr(user, 'profil', None)
        if not profil:
            return False

        # Vérifie si la capacité est disponible pour le rôle de l'utilisateur
        capacities = cls.get_capacities_for_role(profil.role)
        return capacite in capacities

