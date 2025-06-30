import json
from django.core.management.base import BaseCommand
from field.models import Region

class Command(BaseCommand):
    help = 'JSON fayldan regionlarni import qiladi.'

    def handle(self, *args, **kwargs):
        with open('data/regions.json', encoding='utf-8-sig') as f:
            data = json.load(f)
            for item in data:
                Region.objects.update_or_create(
                    id=item['id'],
                    defaults={'name': item['name_uz']}
                )
        self.stdout.write(self.style.SUCCESS("✅ Regionlar muvaffaqiyatli import qilindi."))
