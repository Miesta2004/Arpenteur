from django.contrib import admin

from .models import EvenementSync, WebhookEndpoint


@admin.register(WebhookEndpoint)
class WebhookEndpointAdmin(admin.ModelAdmin):
    list_display = ('nom', 'url', 'actif', 'date_creation')
    list_filter = ('actif',)
    readonly_fields = ('secret',)


@admin.register(EvenementSync)
class EvenementSyncAdmin(admin.ModelAdmin):
    list_display = ('type_objet', 'objet_id', 'action', 'statut_envoi', 'tentatives', 'date_creation')
    list_filter = ('type_objet', 'statut_envoi', 'action')
    readonly_fields = [f.name for f in EvenementSync._meta.fields]

    def has_add_permission(self, request):
        return False
