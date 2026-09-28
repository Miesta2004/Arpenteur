from django.contrib import admin

from .models import Batiment, Caracteristique, Chambre, Etage, Lit, Unite, Zone


@admin.register(Batiment)
class BatimentAdmin(admin.ModelAdmin):
    list_display = ('nom', 'etablissement', 'usage_principal', 'ordre', 'derniere_visite_maj')


@admin.register(Etage)
class EtageAdmin(admin.ModelAdmin):
    list_display = ('nom', 'batiment', 'ordre')


@admin.register(Zone)
class ZoneAdmin(admin.ModelAdmin):
    list_display = ('nom', 'etablissement', 'etage_obj', 'etage_libre', 'a_detail', 'derniere_visite_maj')
    list_filter = ('type',)


@admin.register(Unite)
class UniteAdmin(admin.ModelAdmin):
    list_display = ('nom', 'zone', 'ordre', 'derniere_visite_maj')


@admin.register(Caracteristique)
class CaracteristiqueAdmin(admin.ModelAdmin):
    list_display = ('label', 'code', 'categorie', 'ordre')
    list_filter = ('categorie',)


@admin.register(Chambre)
class ChambreAdmin(admin.ModelAdmin):
    list_display = ('numero', 'type_piece', 'categorie_chambre', 'specialite', 'niveau_confort', 'zone', 'unite', 'avec_lits')
    list_filter = ('type_piece', 'categorie_chambre', 'specialite', 'niveau_confort', 'avec_lits')
    filter_horizontal = ('caracteristiques',)


@admin.register(Lit)
class LitAdmin(admin.ModelAdmin):
    list_display = ('identifiant', 'chambre', 'etat', 'derniere_visite_maj')
    list_filter = ('etat',)
