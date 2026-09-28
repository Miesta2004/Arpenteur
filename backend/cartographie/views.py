from rest_framework import permissions, viewsets

from .models import Batiment, Caracteristique, Chambre, Etage, Lit, Unite, Zone
from .serializers import (
    BatimentSerializer, CaracteristiqueSerializer, ChambreSerializer,
    EtageSerializer, LitSerializer, UniteSerializer, ZoneSerializer,
)


class BatimentViewSet(viewsets.ModelViewSet):
    queryset = Batiment.objects.all()
    serializer_class = BatimentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['etablissement']


class EtageViewSet(viewsets.ModelViewSet):
    queryset = Etage.objects.all()
    serializer_class = EtageSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['batiment']


class ZoneViewSet(viewsets.ModelViewSet):
    queryset = Zone.objects.all()
    serializer_class = ZoneSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['etablissement', 'etage_obj']


class UniteViewSet(viewsets.ModelViewSet):
    queryset = Unite.objects.all()
    serializer_class = UniteSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['zone']


class CaracteristiqueViewSet(viewsets.ModelViewSet):
    queryset = Caracteristique.objects.all()
    serializer_class = CaracteristiqueSerializer
    permission_classes = [permissions.IsAuthenticated]


class ChambreViewSet(viewsets.ModelViewSet):
    queryset = Chambre.objects.all()
    serializer_class = ChambreSerializer
    permission_classes = [permissions.IsAuthenticated]
    # Ces filtres répondent directement aux questions cibles :
    # "chambres VIP" -> ?niveau_confort=vip
    # "chambres compatibles isolement" -> ?specialite=isolement
    # "chambres avec oxygène mural" -> ?caracteristiques__code=oxygene_mural
    filterset_fields = ['zone', 'unite', 'type_piece', 'categorie_chambre', 'specialite', 'niveau_confort', 'caracteristiques']


class LitViewSet(viewsets.ModelViewSet):
    queryset = Lit.objects.all()
    serializer_class = LitSerializer
    permission_classes = [permissions.IsAuthenticated]
    # "lits disponibles" -> ?etat=disponible ; "lits indisponibles" -> ?etat=hors_service (etc.)
    filterset_fields = ['chambre', 'etat']
