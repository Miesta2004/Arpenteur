from rest_framework.routers import DefaultRouter

from .views import CommentaireViewSet, MembreEquipeViewSet, VisiteViewSet

router = DefaultRouter()
router.register(r'visites', VisiteViewSet, basename='visite')
router.register(r'membres-equipe', MembreEquipeViewSet, basename='membre-equipe')
router.register(r'commentaires', CommentaireViewSet, basename='commentaire')

urlpatterns = router.urls
