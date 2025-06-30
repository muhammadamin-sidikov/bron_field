from django.apps import AppConfig
import threading
import time
from datetime import datetime
import pytz

class BronConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bron'

    def ready(self):
        import bron.signals
        from .tasks import update_bron_status

        def start_scheduler():
            uzb_tz = pytz.timezone('Asia/Tashkent')
            while True:
                now = datetime.now(uzb_tz)
                if now.minute in [0, 30]:
                    print(f"Running update_bron_status at {now.strftime('%H:%M')}")
                    update_bron_status()
                time.sleep(60)
        threading.Thread(target=start_scheduler, daemon=True).start()
