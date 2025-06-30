from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework import generics
from .serializers import (
    RegisterSerializer, UserProfileSerializer,
    VerifyEmailSerializer, AdminChangePasswordSerializer,
    UserPasswordListSerializer,
)
from .models import UserProfile
from .permissions import IsOwnerOrAdmin

class RegisterView(APIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            result = serializer.save()
            return Response(result, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyEmailView(APIView):
    permission_classes = [AllowAny]
    serializer_class = VerifyEmailSerializer

    def get(self, request):
        token_str = request.GET.get("token")
        if not token_str:
            return Response({"error": "Token is required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            token = AccessToken(token_str)
            username = token.get('username')
            email = token.get('email')
            password = token.get('password')

            if not all([username, email, password]):
                return Response({"error": "Token is missing required fields."}, status=400)

            user = User.objects.create_user(username=username, email=email, password=password)
            user.is_active = True
            user.save()

            return Response({"detail": "Email verified and user created successfully."})
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileListView(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [AllowAny]

class UserProfileDetailView(generics.RetrieveUpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    lookup_field = 'pk'


class PasswordUserListView(generics.ListAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserPasswordListSerializer

class PasswordUpdateByAdminView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = AdminChangePasswordSerializer
    permission_classes = [IsOwnerOrAdmin]
    lookup_field = "pk"


