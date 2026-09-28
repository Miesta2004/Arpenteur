from django.contrib import admin

from .models import Equipement, MaintenanceEquipement, Photo


class MaintenanceInline(admin.TabularInline):
    model = MaintenanceEquipement
    extra = 0


@admin.register(Equipement)
class EquipementAdmin(admin.ModelAdmin):
    list_display = ('nom', 'categorie', 'etat', 'disponibilite', 'lit', 'chambre', 'zone', 'numero_inventaire')
    list_filter = ('categorie', 'etat', 'disponibilite')
    inlines = [MaintenanceInline]


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('legende', 'etablissement', 'visite', 'chambre', 'equipement', 'date_ajout')
