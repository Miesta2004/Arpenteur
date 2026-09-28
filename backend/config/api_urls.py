from django.urls import path, include

urlpatterns = [
    path('', include('comptes.urls')),
    path('', include('organisations.urls')),
    path('', include('missions.urls')),
    path('', include('cartographie.urls')),
    path('', include('inventaire.urls')),
    path('', include('activites.urls')),
    path('', include('notifications.urls')),
]