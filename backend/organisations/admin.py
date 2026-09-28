from django.contrib import admin

from .models import Etablissement


@admin.register(Etablissement)
class EtablissementAdmin(admin.ModelAdmin):
    list_display = ('nom', 'type', 'statut', 'ville', 'region', 'date_creation')
    list_filter = ('type', 'statut', 'region')
    search_fields = ('nom', 'ville')
