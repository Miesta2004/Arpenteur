from rest_framework.routers import DefaultRouter

from .views import EquipementViewSet, MaintenanceEquipementViewSet, PhotoViewSet

router = DefaultRouter()
router.register(r'equipements', EquipementViewSet, basename='equipement')
router.register(r'maintenances', MaintenanceEquipementViewSet, basename='maintenance')
router.register(r'photos', PhotoViewSet, basename='photo')

urlpatterns = router.urls
