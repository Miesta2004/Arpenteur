from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from cartographie.models import Batiment, Chambre, Lit
from inventaire.models import Equipement

from .models import EvenementSync
from .tasks import envoyer_evenement

# Champs capturés dans le payload de chaque type d'objet — volontairement
# minimal : juste ce qui a une valeur pour HealthTracker (pas les champs
# purement Arpenteur comme les notes internes ou derniere_visite_maj).
CHAMPS_PAYLOAD = {
    Lit: ['id', 'chambre_id', 'identifiant', 'etat'],
    Chambre: [
        'id', 'zone_id', 'unite_id', 'numero', 'type_piece',
        'categorie_chambre', 'specialite', 'niveau_confort', 'avec_lits', 'capacite_prevue',
    ],
    Batiment: ['id', 'etablissement_id', 'nom', 'etat_general'],
    Equipement: ['id', 'nom', 'categorie', 'etat', 'disponibilite', 'lit_id', 'chambre_id', 'zone_id'],
}


def _construire_payload(instance):
    champs = CHAMPS_PAYLOAD.get(type(instance), [])
    return {champ: getattr(instance, champ) for champ in champs}


def _creer_evenement(instance, action):
    evenement = EvenementSync.objects.create(
        type_objet=type(instance).__name__,
        objet_id=instance.pk,
        action=action,
        payload=_construire_payload(instance),
    )
    # .delay() : mise en file Celery, ne bloque jamais la requête HTTP en cours
    # (l'utilisateur qui vient de sauvegarder la chambre n'attend pas que le
    # webhook réponde). Si Celery est indisponible à cet instant, l'événement
    # reste en_attente en base — traiter_file_evenements le rattrapera plus tard.
    envoyer_evenement.delay(evenement.id)


@receiver(post_save, sender=Lit)
@receiver(post_save, sender=Chambre)
@receiver(post_save, sender=Batiment)
@receiver(post_save, sender=Equipement)
def sur_sauvegarde(sender, instance, created, **kwargs):
    _creer_evenement(instance, 'creation' if created else 'modification')


@receiver(post_delete, sender=Lit)
@receiver(post_delete, sender=Chambre)
@receiver(post_delete, sender=Batiment)
@receiver(post_delete, sender=Equipement)
def sur_suppression(sender, instance, **kwargs):
    _creer_evenement(instance, 'suppression')
