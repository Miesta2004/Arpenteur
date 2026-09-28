from rest_framework import serializers

from comptes.serializers import UserSerializer
from .models import JournalActivite



class JournalActiviteSerializer(serializers.ModelSerializer):
    utilisateur = UserSerializer(read_only=True)

    class Meta:
        model = JournalActivite
        fields = '__all__'
