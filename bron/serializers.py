from django.utils import timezone
from rest_framework import serializers
from .models import Bron, Game
from decimal import Decimal

class BronSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    field_name = serializers.ReadOnlyField(source='field.name')

    class Meta:
        model = Bron
        fields = ['id', 'user', 'field', 'field_name', 'situation', 'date', 'bron_created_at']
        read_only_fields = ['user']

    def validate_date(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("O‘tmish uchun bron qilish mumkin emas.")
        if value.minute not in [0, 30]:
            raise serializers.ValidationError("Faqat :00 yoki :30 daqiqa bo'lishi mumkin.")
        return value


class GameSerializer(serializers.ModelSerializer):
    bron_info = serializers.ReadOnlyField(source='bron.__str__')

    class Meta:
        model = Game
        fields = ['id', 'bron_info', 'started_at', 'completed_at', 'price_per_hour', 'bron']

    def create(self, validated_data):
        bron = validated_data['bron']
        validated_data['completed_at'] = timezone.now()

        hours = (validated_data['completed_at'] - validated_data['started_at']).total_seconds() / 3600
        validated_data['price_per_hour'] = round(bron.field.price_per_hour * hours, 2)

        bron.situation = 'completed'
        bron.save()

        return super().create(validated_data)





