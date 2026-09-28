from .models import JournalActivite


def journaliser(user, action_str, objet, description):
    """Écrit une entrée dans le journal d'activité (Partie 8). Appelée explicitement
    depuis les vues de n'importe quelle app — pas de signal automatique (Partie 3,
    §11 : volontairement simple, pas de tracking implicite type django-simple-history)."""
    JournalActivite.objects.create(
        utilisateur=user if getattr(user, 'is_authenticated', False) else None,
        action=action_str,
        objet_type=objet.__class__.__name__,
        objet_id=objet.pk,
        description=description,
    )
