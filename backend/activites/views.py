from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from comptes.permissions import EstResponsableOuAdmin, get_role
from missions.models import StatutVisite, Visite
from missions.serializers import VisiteListSerializer
from organisations.models import Etablissement

from .models import JournalActivite
from .serializers import JournalActiviteSerializer


class JournalActiviteViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = JournalActivite.objects.select_related('utilisateur').all()
    serializer_class = JournalActiviteSerializer
    permission_classes = [EstResponsableOuAdmin]
    filterset_fields = ['objet_type', 'objet_id', 'action']


class TableauDeBordView(APIView):
    """Vue agrégée pour l'écran 2 de la maquette. Vit dans `common` plutôt que dans
    `organizations` ou `missions` parce qu'elle traverse les deux domaines — aucun
    des deux n'en est le propriétaire naturel."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        role = get_role(request.user)
        visites_qs = Visite.objects.all()
        if role == 'visiteur':
            visites_qs = visites_qs.filter(cree_par=request.user)

        data = {
            'nb_etablissements': Etablissement.objects.count(),
            'nb_visites': visites_qs.count(),
            'nb_visites_en_cours': visites_qs.filter(statut=StatutVisite.EN_COURS).count(),
            'nb_rapports_generes': visites_qs.filter(
                statut__in=[StatutVisite.TERMINE, StatutVisite.ENVOYE]
            ).count(),
            'visites_recentes': VisiteListSerializer(
                visites_qs.order_by('-date_modification')[:6], many=True
            ).data,
        }
        return Response(data)
