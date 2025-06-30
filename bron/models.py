from django.db import models
from django.contrib.auth import get_user_model
from field.models import Field

User = get_user_model()

class Bron(models.Model):
    BRON_SITUATION = [
        ('begins', 'Begins'),
        ('started', 'Started'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bron_user')
    field = models.ForeignKey(Field, on_delete=models.CASCADE, related_name='bron_field')
    situation = models.CharField(max_length=20, choices=BRON_SITUATION, default='begins')
    date = models.DateTimeField('YYYY-MM-DD HH:MM')
    bron_created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('field', 'date')

    def __str__(self):
        return f"{self.user.username} → {self.field.name} ({self.date})"


class Game(models.Model):
    bron = models.OneToOneField(Bron, on_delete=models.CASCADE, related_name='game')
    started_at = models.DateTimeField('YYYY-MM-DD HH:MM')
    completed_at = models.DateTimeField('YYYY-MM-DD HH:MM', null=True, blank=True)
    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"Game at {self.bron.field.name} on {self.bron.date}"

