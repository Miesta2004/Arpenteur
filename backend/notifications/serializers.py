from rest_framework import serializers

from .models import EvenementSync, WebhookEndpoint


class WebhookEndpointSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebhookEndpoint
        fields = ['id', 'nom', 'url', 'secret', 'evenements_abonnes', 'actif', 'date_creation']
        read_only_fields = ['secret', 'date_creation']  # généré automatiquement, jamais modifiable par l'API


class EvenementSyncSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvenementSync
        fields = '__all__'
