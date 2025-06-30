from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Field(models.Model):
    FIELD_TYPES = [
        ('football', 'Football'),
        ('basketball', 'Basketball'),
        ('volleyball', 'Volleyball'),
        ('tennis', 'Tennis'),
    ]
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fields')
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=FIELD_TYPES)
    size = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=100)
    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.owner}, {self.name}, {self.location}"

class Region(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class District(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='districts')
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.region.name} — {self.name}"

class FieldLocation(models.Model):
    field = models.ForeignKey(Field, on_delete=models.CASCADE, related_name='locations')
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    address = models.TextField(blank=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f"{self.field}, {self.district}"

class FieldImage(models.Model):
    field = models.ForeignKey(Field, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='field_images/')

    def __str__(self):
        return f"Image of {self.field.name}"

class FieldLike(models.Model):
    field = models.ForeignKey(Field, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('field', 'user')

    def __str__(self):
        return f"{self.user.username} liked {self.field.name}"

class FieldComment(models.Model):
    field = models.ForeignKey(Field, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s comment on {self.field.name}"

class FieldStar(models.Model):
    field = models.ForeignKey(Field, on_delete=models.CASCADE, related_name='stars')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=1)

    class Meta:
        unique_together = ('field', 'user')

    def __str__(self):
        return f"{self.user.username} rated {self.field.name} as {self.rating}"

