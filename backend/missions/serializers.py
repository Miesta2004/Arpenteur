from django.contrib.auth.models import User
from rest_framework import serializers

from comptes.serializers import UserSerializer
from inventaire.serializers import PhotoSerializer

from .models import Commentaire, MembreEquipe, Visite


class MembreEquipeSerializer(serializers.ModelSerializer):
    utilisateur = UserSerializer(read_only=True)
    utilisateur_id = serializers.PrimaryKeyRelatedField(
        source='utilisateur', queryset=User.objects.all(), write_only=True
    )

    class Meta:
        model = MembreEquipe
        fields = ['id', 'visite', 'utilisateur', 'utilisateur_id', 'est_inspecteur_principal']


class CommentaireSerializer(serializers.ModelSerializer):
    auteur = UserSerializer(read_only=True)

    class Meta:
        model = Commentaire
        fields = ['id', 'visite', 'auteur', 'texte', 'date_creation']
        read_only_fields = ['auteur', 'date_creation']


class VisiteListSerializer(serializers.ModelSerializer):
    """Pour le tableau de bord et la liste des visites (écrans 2 et 3)."""
    etablissement_nom = serializers.CharField(source='etablissement.nom', read_only=True)
    avancement = serializers.IntegerField(read_only=True)

    class Meta:
        model = Visite
        fields = ['id', 'etablissement', 'etablissement_nom', 'date_visite', 'statut', 'avancement']


class VisiteDetailSerializer(serializers.ModelSerializer):
    membres_equipe = MembreEquipeSerializer(many=True, read_only=True)
    photos = PhotoSerializer(many=True, read_only=True)
    commentaires = CommentaireSerializer(many=True, read_only=True)

    avancement = serializers.IntegerField(read_only=True)
    nb_batiments = serializers.IntegerField(read_only=True)
    nb_zones = serializers.IntegerField(read_only=True)
    nb_chambres = serializers.IntegerField(read_only=True)
    nb_lits = serializers.IntegerField(read_only=True)

    class Meta:
        model = Visite
        fields = '__all__'
        read_only_fields = ['cree_par', 'date_creation', 'date_modification']
