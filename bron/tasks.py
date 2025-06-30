from django.utils import timezone
from bron.models import Bron, Game

def update_bron_status():
    now = timezone.localtime()

    bron_qs = Bron.objects.select_related('game').filter(situation__in=['begins', 'started'])
    updated_count = 0

    for bron in bron_qs:
        game = getattr(bron, 'game', None)
        if not game:
            continue

        if bron.situation == 'begins' and game.started_at <= now:
            bron.situation = 'started'
            bron.save()
            # print(f"{bron.id}: begins → started")
            updated_count += 1

        elif bron.situation == 'started' and game.completed_at and game.completed_at <= now:
            bron.situation = 'completed'
            bron.save()
            # print(f"{bron.id}: started → completed")
            updated_count += 1

    # print(f"{updated_count} bron(s) updated.")
    # print(now)