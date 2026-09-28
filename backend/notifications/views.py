from rest_framework import viewsets

from comptes.permissions import EstAdmin

from .models import EvenementSync, WebhookEndpoint
from .serializers import EvenementSyncSerializer, WebhookEndpointSerializer


class WebhookEndpointViewSet(viewsets.ModelViewSet):
    """Réservé aux admins : un webhook mal configuré peut envoyer des données de
    l'établissement vers n'importe quelle URL — ce n'est pas une action anodine."""
    queryset = WebhookEndpoint.objects.all()
    serializer_class = WebhookEndpointSerializer
    permission_classes = [EstAdmin]


class EvenementSyncViewSet(viewsets.ReadOnlyModelViewSet):
    """Lecture seule — sert à auditer/déboguer la file d'événements, jamais à la
    modifier depuis l'API (seule la tâche Celery écrit dessus)."""
    queryset = EvenementSync.objects.all()
    serializer_class = EvenementSyncSerializer
    permission_classes = [EstAdmin]
    filterset_fields = ['type_objet', 'statut_envoi']
