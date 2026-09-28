from rest_framework.routers import DefaultRouter

from .views import EvenementSyncViewSet, WebhookEndpointViewSet

router = DefaultRouter()
router.register(r'webhooks', WebhookEndpointViewSet, basename='webhook')
router.register(r'evenements-sync', EvenementSyncViewSet, basename='evenement-sync')

urlpatterns = router.urls
