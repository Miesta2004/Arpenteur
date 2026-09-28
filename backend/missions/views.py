from django.utils import timezone
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from comptes.permissions import EstResponsableOuAdmin
from activites.utils import journaliser

from .models import Commentaire, MembreEquipe, StatutVisite, Visite
from .serializers import (
    CommentaireSerializer, MembreEquipeSerializer,
    VisiteDetailSerializer, VisiteListSerializer,
)


class VisiteViewSet(viewsets.ModelViewSet):
    queryset = Visite.objects.select_related('etablissement').all()
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['statut', 'etablissement']

    def get_serializer_class(self):
        if self.action == 'list':
            return VisiteListSerializer
        return VisiteDetailSerializer

    def perform_create(self, serializer):
        visite = serializer.save(
            cree_par=self.request.user,
            auteur=self.request.user.get_full_name() or self.request.user.username,
        )
        journaliser(self.request.user, 'creation', visite, f"Visite créée pour {visite.etablissement.nom}")

    def perform_update(self, serializer):
        visite = serializer.save()
        journaliser(self.request.user, 'modification', visite, "Visite modifiée")

    @action(detail=True, methods=['post'], permission_classes=[EstResponsableOuAdmin])
    def valider(self, request, pk=None):
        """Passage au statut Validé — réservé au Responsable de mission / Admin (Partie 2)."""
        visite = self.get_object()
        visite.statut = StatutVisite.ENVOYE
        visite.save(update_fields=['statut'])
        journaliser(request.user, 'validation', visite, "Visite validée")
        return Response(VisiteDetailSerializer(visite).data)

    @action(detail=True, methods=['post'])
    def dupliquer(self, request, pk=None):
        """Raccourci "visite de suivi" : crée une nouvelle visite brouillon pour le
        même établissement. Ne copie plus la cartographie (Partie 3 révisée) — elle
        est désormais partagée au niveau de l'établissement, donc déjà visible pour
        la nouvelle visite sans duplication."""
        source = self.get_object()
        nouvelle = Visite.objects.create(
            etablissement=source.etablissement,
            date_visite=timezone.now().date(),
            statut=StatutVisite.BROUILLON,
            cree_par=request.user,
            auteur=request.user.get_full_name() or request.user.username,
        )
        journaliser(request.user, 'creation', nouvelle, f"Visite de suivi créée depuis #{source.pk}")
        return Response(VisiteDetailSerializer(nouvelle).data, status=status.HTTP_201_CREATED)


class MembreEquipeViewSet(viewsets.ModelViewSet):
    queryset = MembreEquipe.objects.select_related('utilisateur', 'visite')
    serializer_class = MembreEquipeSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['visite']


class CommentaireViewSet(viewsets.ModelViewSet):
    queryset = Commentaire.objects.select_related('auteur').all()
    serializer_class = CommentaireSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['visite']

    def perform_create(self, serializer):
        commentaire = serializer.save(auteur=self.request.user)
        journaliser(self.request.user, 'creation', commentaire, "Commentaire ajouté sur la visite")
