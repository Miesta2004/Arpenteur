from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import JournalActiviteViewSet, TableauDeBordView

router = DefaultRouter()
router.register(r'journal', JournalActiviteViewSet, basename='journal')

urlpatterns = [
                  path('tableau-de-bord/', TableauDeBordView.as_view(), name='tableau-de-bord'),
              ] + router.urls
