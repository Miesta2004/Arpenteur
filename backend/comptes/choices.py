from django.db import models


class EtatLocaux(models.TextChoices):
    """Partagé entre missions.Visite (etat_locaux) et cartography.Batiment
    (etat_general) — d'où sa place ici plutôt que dans l'une ou l'autre app."""
    BON = 'bon', 'Bon état'
    MOYEN = 'moyen', 'État moyen'
    DEGRADE = 'degrade', 'Dégradé'
    A_RENOVER = 'a_renover', 'À rénover'
