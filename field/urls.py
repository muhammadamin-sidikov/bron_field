from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AllLocatedFieldsView,
    LocationRegionListView,
    LocationDistrictByPkView,
    LocationDistrictByNameView,
    FieldByNameLocationView,
    FieldByPkLocationView,
    FieldCommentViewSet,
    FieldStatusView,
    FieldStarViewSet,
    FieldLikeViewSet,
    FieldViewSet,
)

router = DefaultRouter()
router.register(r'fields', FieldViewSet, basename='field')
router.register(r'likes', FieldLikeViewSet, basename='field-like')
router.register(r'comments', FieldCommentViewSet, basename='comment')
router.register(r'stars', FieldStarViewSet, basename='star')

urlpatterns = [
    path('', include(router.urls)),

    path('located/', AllLocatedFieldsView.as_view()),

    path('location/', LocationRegionListView.as_view()),
    path('location/<int:region_pk>/', LocationDistrictByPkView.as_view()),
    path('location/<str:region_name>/', LocationDistrictByNameView.as_view()),

    path('location/<int:region_pk>/<int:district_pk>/', FieldByPkLocationView.as_view()),
    path('location/<str:region_name>/<str:district_name>/', FieldByNameLocationView.as_view()),

    path('status/', FieldStatusView.as_view(), name='field-status'),
]

urlpatterns += router.urls


