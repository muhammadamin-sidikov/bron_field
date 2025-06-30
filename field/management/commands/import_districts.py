import json
from django.core.management.base import BaseCommand
from field.models import District, Region

class Command(BaseCommand):
    help = 'JSON fayldan districtlarni import qiladi.'

    def handle(self, *args, **kwargs):
        with open('data/districts.json', encoding='utf-8-sig') as f:
            data = json.load(f)
            for item in data:
                try:
                    region = Region.objects.get(id=item['region_id'])
                except Region.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f"⚠️ Region ID {item['region_id']} topilmadi."))
                    continue
                District.objects.update_or_create(
                    id=item['id'],
                    defaults={
                        'region': region,
                        'name': item['name_uz']
                    }
                )
        self.stdout.write(self.style.SUCCESS("✅ Tumanlar muvaffaqiyatli import qilindi."))
