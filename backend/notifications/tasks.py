import hashlib
import hmac
import json

import requests
from celery import shared_task
from django.utils import timezone

from .models import EvenementSync, StatutEnvoi, WebhookEndpoint

MAX_TENTATIVES = 5


def _signer(secret: str, corps: bytes) -> str:
    """Signature HMAC-SHA256 du corps de la requête — permet à HealthTracker de
    vérifier que l'appel vient bien d'Arpenteur (comparaison en en-tête X-Signature)."""
    return hmac.new(secret.encode(), corps, hashlib.sha256).hexdigest()


def _livrer(evenement: EvenementSync) -> None:
    """Envoie un événement à tous les webhooks actifs qui y sont abonnés, et met
    à jour son statut. Fonction interne partagée par les deux tâches ci-dessous —
    ni l'une ni l'autre ne duplique la logique d'envoi."""
    destinataires = [w for w in WebhookEndpoint.objects.filter(actif=True) if w.interesse_par(evenement.type_objet)]

    if not destinataires:
        # Personne n'est abonné à ce type d'événement — pas un échec, juste rien à faire.
        evenement.statut_envoi = StatutEnvoi.ENVOYE
        evenement.save(update_fields=['statut_envoi'])
        return

    corps = json.dumps({
        'type_objet': evenement.type_objet,
        'objet_id': evenement.objet_id,
        'action': evenement.action,
        'payload': evenement.payload,
        'date': evenement.date_creation.isoformat(),
    }).encode()

    succes_global = True
    for webhook in destinataires:
        try:
            reponse = requests.post(
                webhook.url,
                data=corps,
                headers={
                    'Content-Type': 'application/json',
                    'X-Signature': _signer(webhook.secret, corps),
                },
                timeout=5,
            )
            reponse.raise_for_status()
        except requests.RequestException:
            succes_global = False

    evenement.tentatives += 1
    evenement.date_dernier_essai = timezone.now()
    evenement.statut_envoi = StatutEnvoi.ENVOYE if succes_global else StatutEnvoi.ECHEC
    evenement.save(update_fields=['tentatives', 'date_dernier_essai', 'statut_envoi'])


@shared_task
def envoyer_evenement(evenement_id: int):
    """Chemin principal : déclenchée immédiatement par le signal (voir
    notifications/signals.py) dès qu'un Lit/Chambre/Bâtiment/Équipement change.
    C'est ce qui rend la synchronisation "temps réel" plutôt que dépendante d'un
    balayage périodique."""
    try:
        evenement = EvenementSync.objects.get(pk=evenement_id, statut_envoi=StatutEnvoi.EN_ATTENTE)
    except EvenementSync.DoesNotExist:
        return  # déjà traité, ou id invalide — rien à faire
    _livrer(evenement)


@shared_task
def traiter_file_evenements():
    """Filet de sécurité : à planifier périodiquement (ex. toutes les 5 minutes
    via Celery beat, voir CELERY_BEAT_SCHEDULE dans settings.py). Rattrape les
    événements qui ont échoué (webhook indisponible un instant) ou qui n'ont
    jamais été traités (Celery hors service au moment du signal) — le dispatch
    immédiat (envoyer_evenement) reste le chemin normal, ceci ne fait que
    nettoyer ce qui serait passé entre les mailles du filet."""
    evenements = EvenementSync.objects.filter(
        statut_envoi__in=[StatutEnvoi.EN_ATTENTE, StatutEnvoi.ECHEC],
        tentatives__lt=MAX_TENTATIVES,
    )
    for evenement in evenements:
        _livrer(evenement)
