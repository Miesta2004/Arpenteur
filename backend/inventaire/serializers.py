from rest_framework import serializers

from .models import Equipement, MaintenanceEquipement, Photo


class MaintenanceEquipementSerializer(serializers.ModelSerializer):
    type_intervention_display = serializers.CharField(source='get_type_intervention_display', read_only=True)

    class Meta:
        model = MaintenanceEquipement
        fields = ['id', 'equipement', 'type_intervention', 'type_intervention_display', 'date', 'technicien', 'description', 'prochain_controle']


class EquipementSerializer(serializers.ModelSerializer):
    disponibilite_display = serializers.CharField(source='get_disponibilite_display', read_only=True)
    interventions = MaintenanceEquipementSerializer(many=True, read_only=True)

    class Meta:
        model = Equipement
        fields = '__all__'

    def validate(self, attrs):
        lit = attrs.get('lit') or getattr(self.instance, 'lit', None)
        chambre = attrs.get('chambre') or getattr(self.instance, 'chambre', None)
        zone = attrs.get('zone') or getattr(self.instance, 'zone', None)
        if not any([lit, chambre, zone]):
            raise serializers.ValidationError(
                "Un équipement doit être rattaché à un lit, une chambre ou un service."
            )
        return attrs


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = '__all__'

    def validate(self, attrs):
        cibles = [attrs.get(c) for c in ('etablissement', 'visite', 'chambre', 'equipement')]
        if not any(cibles) and not any(
                getattr(self.instance, c, None) for c in ('etablissement_id', 'visite_id', 'chambre_id', 'equipement_id')
        ):
            raise serializers.ValidationError(
                "Une photo doit être rattachée à un établissement, une visite, une chambre ou un équipement."
            )
        return attrs
