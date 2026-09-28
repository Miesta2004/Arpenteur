from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Profil


class UserSerializer(serializers.ModelSerializer):
    """Réutilisé par toutes les apps pour représenter un utilisateur imbriqué
    (membres d'équipe, auteur de commentaire...) — jamais le mot de passe."""

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class ProfilSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profil
        fields = ['id', 'user', 'role']
