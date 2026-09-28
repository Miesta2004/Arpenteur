from rest_framework.routers import DefaultRouter

from .views import (
    BatimentViewSet, CaracteristiqueViewSet, ChambreViewSet, EtageViewSet,
    LitViewSet, UniteViewSet, ZoneViewSet,
)

router = DefaultRouter()
router.register(r'batiments', BatimentViewSet, basename='batiment')
router.register(r'etages', EtageViewSet, basename='etage')
router.register(r'zones', ZoneViewSet, basename='zone')
router.register(r'unites', UniteViewSet, basename='unite')
router.register(r'chambres', ChambreViewSet, basename='chambre')
router.register(r'lits', LitViewSet, basename='lit')
router.register(r'caracteristiques', CaracteristiqueViewSet, basename='caracteristique')

urlpatterns = router.urls
