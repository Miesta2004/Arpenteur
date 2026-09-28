from rest_framework import serializers

from cartographie.models import Zone
from cartographie.serializers import BatimentSerializer, ZoneSerializer

from .models import Etablissement


class EtablissementListSerializer(serializers.ModelSerializer):
    """Version allégée pour la liste (écran 3 de la maquette).
    derniere_visite_date vient d'une annotation SQL (Max), pas de la @property du
    modèle — sinon chaque ligne de la liste déclencherait sa propre requête (N+1)."""
    derniere_visite_date = serializers.DateField(read_only=True)

    class Meta:
        model = Etablissement
        fields = ['id', 'nom', 'type', 'statut', 'ville', 'region', 'derniere_visite_date']


class EtablissementSerializer(serializers.ModelSerializer):
    """Version complète : inclut toute la cartographie (Partie 3 révisée), puisque
    bâtiments/étages/services/chambres sont rattachés à l'établissement, partagés
    entre toutes ses visites — plus dupliqués par visite."""
    derniere_visite_date = serializers.DateField(source='derniere_visite.date_visite', read_only=True)
    batiments = BatimentSerializer(many=True, read_only=True)
    zones_sans_etage = serializers.SerializerMethodField()

    # Compteurs "Résumé" (écran 4)
    nb_batiments = serializers.IntegerField(read_only=True)
    nb_etages = serializers.IntegerField(read_only=True)
    nb_services = serializers.IntegerField(read_only=True)
    nb_chambres = serializers.IntegerField(read_only=True)
    nb_lits = serializers.IntegerField(read_only=True)
    nb_equipements = serializers.IntegerField(read_only=True)

    class Meta:
        model = Etablissement
        fields = '__all__'

    def get_zones_sans_etage(self, obj):
        """Services créés en mode rapide (etage_libre texte), pas encore rattachés
        à un étage structuré — n'apparaîtraient pas dans l'arbre batiments->etages->zones."""
        zones = Zone.objects.filter(etablissement=obj, etage_obj__isnull=True)
        return ZoneSerializer(zones, many=True).data
