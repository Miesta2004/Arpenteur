from django.contrib import admin

from .models import JournalActivite


@admin.register(JournalActivite)
class JournalActiviteAdmin(admin.ModelAdmin):
    list_display = ('date', 'utilisateur', 'action', 'objet_type', 'objet_id', 'description')
    list_filter = ('action', 'objet_type')
    readonly_fields = [f.name for f in JournalActivite._meta.fields]

    def has_add_permission(self, request):
        return False
