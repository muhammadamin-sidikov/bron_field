from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    BronViewSet, GameViewSet,
    CancelGameView,
    TopPlayersView,
    TopFieldsView,
)

router = DefaultRouter()
router.register(r'bron', BronViewSet)
router.register(r'game', GameViewSet)

urlpatterns = [
    path('', include(router.urls)),

    path('stats/top-users/', TopPlayersView.as_view()),
    path('stats/top-fields/', TopFieldsView.as_view()),

    path('game/<int:pk>/canceled/', CancelGameView.as_view(), name='cancel-bron'),
]