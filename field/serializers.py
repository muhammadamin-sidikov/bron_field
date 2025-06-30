from rest_framework import serializers
from .models import (
    Field, Region,
    District, FieldLocation,
    FieldLike, FieldComment,
    FieldStar,
)

class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ['id', 'name']

class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ['id', 'name']

class FieldLocationSerializer(serializers.ModelSerializer):
    district = serializers.StringRelatedField()  # ko‘rsatish uchun
    class Meta:
        model = FieldLocation
        fields = ['id', 'district', 'address']

class FieldSerializer(serializers.ModelSerializer):
    locations = FieldLocationSerializer(many=True, read_only=True)
    class Meta:
        model = Field
        fields = ['id', 'name', 'owner', 'locations']

class FieldCreateSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Field
        fields = '__all__'

class FieldLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FieldLike
        fields = ['id', 'field', 'user']
        read_only_fields = ['id', 'user']

class FieldCommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = FieldComment
        fields = ['id', 'field', 'user', 'comment', 'created_at']
        read_only_fields = ['user', 'created_at']

class FieldStarSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(min_value=1, max_value=5)
    class Meta:
        model = FieldStar
        fields = ['id', 'field', 'user', 'rating']
        read_only_fields = ['user']
