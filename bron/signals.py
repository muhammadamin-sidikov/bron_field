from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Bron, Game
from datetime import timedelta

@receiver(post_save, sender=Bron)
def create_game_for_bron(sender, instance, created, **kwargs):
    if created:
        Game.objects.create(
            bron=instance,
            started_at=instance.date,
            completed_at=instance.date + timedelta(hours=1)
        )