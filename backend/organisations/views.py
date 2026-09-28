from django.db.models import Max, Q
from rest_framework import permissions, viewsets

from comptes.permissions import get_role

from .models import Etablissement
from .serializers import EtablissementListSerializer, EtablissementSerializer


class EtablissementViewSet(viewsets.ModelViewSet):
    queryset = Etablissement.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['type', 'region', 'ville']
    search_fields = ['nom', 'ville']

    def get_serializer_class(self):
        if self.action == 'list':
            return EtablissementListSerializer
        return EtablissementSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        if self.action == 'list':
            # Annotation SQL (Max) plutôt que la @property du modèle : évite le
            # N+1 (une requête séparée par établissement affiché dans la liste).
            # .order_by() réappliqué explicitement : annotate(Max(...)) réinitialise
            # l'ordre par défaut du modèle (comportement connu de l'ORM Django).
            qs = qs.annotate(derniere_visite_date=Max('visites__date_visite')).order_by('nom')
        if self.action == 'retrieve':
            qs = qs.prefetch_related(
                'batiments__etages__zones__chambres__lits',
                'batiments__etages__zones__chambres__equipements_lies',
                'zones__chambres__lits',  # services en mode rapide (etage_libre, sans etage_obj)
            )
        recherche = self.request.query_params.get('q')
        if recherche:
            qs = qs.filter(Q(nom__icontains=recherche) | Q(ville__icontains=recherche))
        return qs

    def perform_destroy(self, instance):
        if get_role(self.request.user) != 'admin':
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Seul un administrateur peut supprimer un établissement.")
        instance.delete()
