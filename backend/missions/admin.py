from django.contrib import admin

from .models import Commentaire, MembreEquipe, Visite


class MembreEquipeInline(admin.TabularInline):
    model = MembreEquipe
    extra = 1


@admin.register(Visite)
class VisiteAdmin(admin.ModelAdmin):
    list_display = ('etablissement', 'date_visite', 'statut', 'avancement')
    list_filter = ('statut',)
    inlines = [MembreEquipeInline]


@admin.register(Commentaire)
class CommentaireAdmin(admin.ModelAdmin):
    list_display = ('visite', 'auteur', 'date_creation')
    list_filter = ('date_creation',)
