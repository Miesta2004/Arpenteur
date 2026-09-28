from rest_framework import serializers

from inventaire.serializers import EquipementSerializer

from .models import Batiment, Caracteristique, Chambre, Etage, Lit, Unite, Zone


class CaracteristiqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Caracteristique
        fields = ['id', 'code', 'label', 'categorie', 'ordre']


class LitSerializer(serializers.ModelSerializer):
    etat_display = serializers.CharField(source='get_etat_display', read_only=True)
    est_utilisable = serializers.BooleanField(read_only=True)

    class Meta:
        model = Lit
        fields = ['id', 'chambre', 'identifiant', 'etat', 'etat_display', 'est_utilisable', 'equipements', 'derniere_visite_maj']


class ChambreSerializer(serializers.ModelSerializer):
    lits = LitSerializer(many=True, read_only=True)
    equipements_lies = EquipementSerializer(many=True, read_only=True)
    type_piece_display = serializers.CharField(source='get_type_piece_display', read_only=True)
    categorie_chambre_display = serializers.CharField(source='get_categorie_chambre_display', read_only=True)
    specialite_display = serializers.CharField(source='get_specialite_display', read_only=True)
    niveau_confort_display = serializers.CharField(source='get_niveau_confort_display', read_only=True)

    caracteristiques = CaracteristiqueSerializer(many=True, read_only=True)
    caracteristiques_ids = serializers.PrimaryKeyRelatedField(
        source='caracteristiques', queryset=Caracteristique.objects.all(),
        many=True, write_only=True, required=False,
    )

    class Meta:
        model = Chambre
        fields = [
            'id', 'zone', 'unite', 'numero', 'type_piece', 'type_piece_display', 'avec_lits',
            'categorie_chambre', 'categorie_chambre_display', 'specialite', 'specialite_display',
            'niveau_confort', 'niveau_confort_display', 'caracteristiques', 'caracteristiques_ids',
            'capacite_prevue', 'notes', 'derniere_visite_maj', 'lits', 'equipements_lies',
        ]


class UniteSerializer(serializers.ModelSerializer):
    chambres = ChambreSerializer(many=True, read_only=True)

    class Meta:
        model = Unite
        fields = '__all__'


class ZoneSerializer(serializers.ModelSerializer):
    # Seulement les chambres rattachées directement au service (mode rapide, sans
    # Unité) — celles qui appartiennent à une Unité apparaissent sous
    # unites[].chambres, pas ici, pour éviter qu'une même chambre soit listée deux fois.
    chambres = serializers.SerializerMethodField()
    unites = UniteSerializer(many=True, read_only=True)
    a_detail = serializers.BooleanField(read_only=True)
    nb_chambres_detaillees = serializers.IntegerField(read_only=True)

    class Meta:
        model = Zone
        fields = '__all__'

    def get_chambres(self, obj):
        return ChambreSerializer(obj.chambres.filter(unite__isnull=True), many=True).data


class EtageSerializer(serializers.ModelSerializer):
    zones = ZoneSerializer(many=True, read_only=True)

    class Meta:
        model = Etage
        fields = '__all__'


class BatimentSerializer(serializers.ModelSerializer):
    etages = EtageSerializer(many=True, read_only=True)

    class Meta:
        model = Batiment
        fields = '__all__'
