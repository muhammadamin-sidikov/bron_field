from django.urls import path
from .views import (
    VerifyEmailView, RegisterView,
    UserProfileListView, UserProfileDetailView,
    PasswordUpdateByAdminView, PasswordUserListView,
)

urlpatterns = [
    path('profile/', UserProfileListView.as_view(), name='user-profile'),
    path('profile/<int:pk>/', UserProfileDetailView.as_view(), name='profile-detail'),

    path('change-password/', PasswordUserListView.as_view(), name='change-password'),
    path('change-password/<int:pk>/', PasswordUpdateByAdminView.as_view(), name='password-update'),

    path('register/', RegisterView.as_view(), name='register'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify-email'),
]