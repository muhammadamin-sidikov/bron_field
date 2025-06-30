from rest_framework import viewsets, permissions, status
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from decimal import Decimal
from django.db.models import Count
from .models import Bron, Game, Field
from .serializers import (
    BronSerializer, GameSerializer,
)

User = get_user_model()

class BronViewSet(viewsets.ModelViewSet):
    queryset = Bron.objects.all()
    serializer_class = BronSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CancelGameView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            game = Game.objects.get(pk=pk)
        except Game.DoesNotExist:
            return Response({"detail": "Game topilmadi."}, status=status.HTTP_404_NOT_FOUND)

        bron = game.bron
        if bron.situation == 'completed':
            return Response({"detail": "Bu o‘yin allaqachon yakunlangan."}, status=status.HTTP_400_BAD_REQUEST)

        bron.situation = 'canceled'
        bron.save()

        return Response({"detail": "Game bekor qilindi, bron holati 'canceled'ga o‘zgardi."}, status=status.HTTP_200_OK)

class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'post', 'patch', 'put']

    def perform_update(self, serializer):
        game = serializer.save()
        bron = game.bron

        if game.completed_at and game.started_at:
            delta = game.completed_at - game.started_at
            hours = delta.total_seconds() / 3600
            price = bron.field.price_per_hour * Decimal(str(hours))
            game.price_per_hour = round(price, 2)
            game.save()

class TopPlayersView(APIView):
    def get(self, request):
        top_users = User.objects.annotate(
            games_count=Count('bron_user__game')
        ).order_by('-games_count')[:3]

        data = [
            {
                "user_id": user.id,
                "username": user.username,
                "games_played": user.games_count
            }
            for user in top_users
        ]

        return Response(data)

class TopFieldsView(APIView):
    def get(self, request):
        top_fields = Field.objects.annotate(
            games_count=Count('bron_field__game')
        ).order_by('-games_count')[:3]

        data = [
            {
                "field_id": field.id,
                "field_name": field.name,
                "games_played": field.games_count
            }
            for field in top_fields
        ]

        return Response(data)


