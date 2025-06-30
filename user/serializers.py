from rest_framework import serializers
from django.contrib.auth.models import User
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken
from .models import UserProfile

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError("Email already exists.")
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError("Username already exists.")
        return data

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            is_active=False
        )
        user.set_password(validated_data['password1'])

        token = RefreshToken.for_user(user)
        token['username'] = validated_data['username']
        token['email'] = validated_data['email']
        token['password'] = validated_data['password1']

        verify_link = f"http://127.0.0.1:8000/api/user/verify-email/?token={str(token.access_token)}"

        send_mail(
            "Verify your email",
            f"Click to verify your account: {verify_link}",
            "noreply@yourapp.com",
            [validated_data['email']],
            fail_silently=False,
        )

        return {"detail": "Verification link sent to your email."}

class VerifyEmailSerializer(serializers.Serializer):
    token = serializers.CharField(help_text="Email orqali yuborilgan JWT token")

class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', required=False)
    email = serializers.EmailField(source='user.email', required=False)

    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'email', 'profile_image', 'phone', 'birth_date', 'gender']

    def validate(self, attrs):
        user_data = attrs.get('user', {})
        username = user_data.get('username')
        email = user_data.get('email')
        phone = attrs.get('phone')

        user = self.instance.user if self.instance else None

        if username and User.objects.exclude(pk=user.pk).filter(username=username).exists():
            raise serializers.ValidationError({"username": "This username is already taken."})

        if email and User.objects.exclude(pk=user.pk).filter(email=email).exists():
            raise serializers.ValidationError({"email": "This email is already registered."})

        if phone and UserProfile.objects.exclude(pk=self.instance.pk).filter(phone=phone).exists():
            raise serializers.ValidationError({"phone": "This phone number is already in use."})

        return attrs

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        username = user_data.get('username')
        email = user_data.get('email')

        if username:
            instance.user.username = username
        if email:
            instance.user.email = email
        instance.user.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class UserPasswordListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class AdminChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password1 = serializers.CharField(write_only=True)
    new_password2 = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['new_password1'] != data['new_password2']:
            raise serializers.ValidationError("Yangi parollar mos emas.")
        if data['new_password1'] == data['old_password']:
            raise serializers.ValidationError("Bu eski parol")
        return data

    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password1'])
        instance.save()
        return instance
