from rest_framework import permissions, viewsets

from .models import Equipement, MaintenanceEquipement, Photo
from .serializers import EquipementSerializer, MaintenanceEquipementSerializer, PhotoSerializer


class EquipementViewSet(viewsets.ModelViewSet):
    queryset = Equipement.objects.all()
    serializer_class = EquipementSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['lit', 'chambre', 'zone', 'etat', 'categorie', 'disponibilite']
    search_fields = ['nom', 'numero_inventaire']


class MaintenanceEquipementViewSet(viewsets.ModelViewSet):
    queryset = MaintenanceEquipement.objects.select_related('equipement').all()
    serializer_class = MaintenanceEquipementSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['equipement', 'type_intervention']


class PhotoViewSet(viewsets.ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['etablissement', 'visite', 'chambre', 'equipement']
