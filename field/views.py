from django.shortcuts import get_object_or_404
from django.db.models import Count, Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import filters
from .permissions import IsOwnerOrAdmin
from .filters import FieldFilter, FieldStatusFilter
from .serializers import (
    FieldCreateSerializer, RegionSerializer,
    DistrictSerializer, FieldSerializer,
    FieldLikeSerializer, FieldCommentSerializer,
    FieldStarSerializer
)
from .models import (
    Field, Region,
    District, FieldLocation,
    FieldLike, FieldComment,
    FieldStar
)

class LocationRegionListView(APIView):
    def get(self, request):
        regions = Region.objects.all()
        serializer = RegionSerializer(regions, many=True)
        return Response(serializer.data)

class LocationDistrictByPkView(APIView):
    def get(self, request, region_pk):
        region = get_object_or_404(Region, pk=region_pk)
        districts = District.objects.filter(region=region)
        serializer = DistrictSerializer(districts, many=True)
        return Response({
            "region": region.name,
            "districts": serializer.data
        })

class LocationDistrictByNameView(APIView):
    def get(self, request, region_name):
        region = get_object_or_404(Region, name__iexact=region_name)
        districts = District.objects.filter(region=region)
        serializer = DistrictSerializer(districts, many=True)
        return Response({
            "region": region.name,
            "districts": serializer.data
        })


class FieldByPkLocationView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    def get(self, request, region_pk, district_pk):
        region = get_object_or_404(Region, pk=region_pk)
        district = get_object_or_404(District, pk=district_pk, region=region)

        located_fields_qs = Field.objects.filter(locations__district=district).distinct()

        if request.user.is_staff:
            unlocated_fields_qs = Field.objects.exclude(
                locations__district__region=region
            ).distinct()
        else:
            unlocated_fields_qs = Field.objects.filter(owner=request.user).exclude(
                locations__district__region=region
            ).distinct()

        located_fields = [
            {
                "id": f.id,
                "name": f.name,
                "address": f.locations.filter(district=district).first().address
                if f.locations.filter(district=district).exists()
                else None
            }
            for f in located_fields_qs
        ]

        unlocated_fields = [
            {
                "id": f.id,
                "name": f.name,
                "address": None
            } for f in unlocated_fields_qs
        ]

        return Response({
            "located_fields": located_fields,
            "unlocated_fields": unlocated_fields,
        })

    def put(self, request, region_pk, district_pk):
        field_id = request.data.get('field')
        address = request.data.get('address', '')

        district = get_object_or_404(District, pk=district_pk, region__pk=region_pk)
        field = get_object_or_404(Field, pk=field_id)

        self.check_object_permissions(request, field)

        existing_location = FieldLocation.objects.filter(field=field).exclude(district=district).first()
        if existing_location:
            return Response(
                {"error": f"Field allaqachon '{existing_location.district.name}' tumanga joylashtirilgan"},
                status=status.HTTP_400_BAD_REQUEST
            )

        FieldLocation.objects.update_or_create(
            field=field,
            district=district,
            defaults={"address": address}
        )

        return Response({"message": "Field joylashtirildi"}, status=status.HTTP_200_OK)

    def delete(self, request, region_pk, district_pk):
        field_id = request.data.get('field')
        district = get_object_or_404(District, pk=district_pk, region__pk=region_pk)
        field = get_object_or_404(Field, pk=field_id)

        # 🔒 Permission check
        self.check_object_permissions(request, field)

        location_qs = FieldLocation.objects.filter(field=field, district=district)
        if not location_qs.exists():
            return Response(
                {"error": "Bu field ushbu tumanga biriktirilmagan"},
                status=status.HTTP_400_BAD_REQUEST
            )

        location_qs.delete()
        return Response({"message": "Field lokatsiyadan olib tashlandi"}, status=status.HTTP_200_OK)

class FieldByNameLocationView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    def get(self, request, region_name, district_name):
        region = get_object_or_404(Region, name__iexact=region_name)
        district = get_object_or_404(District, name__iexact=district_name, region=region)

        located_fields_qs = Field.objects.filter(locations__district=district).distinct()

        if request.user.is_staff:
            unlocated_fields_qs = Field.objects.exclude(
                locations__district__region=region
            ).distinct()
        else:
            unlocated_fields_qs = Field.objects.filter(owner=request.user).exclude(
                locations__district__region=region
            ).distinct()

        located_fields = [
            {
                "id": f.id,
                "name": f.name,
                "address": f.locations.filter(district=district).first().address
                if f.locations.filter(district=district).exists()
                else None
            }
            for f in located_fields_qs
        ]

        unlocated_fields = [
            {
                "id": f.id,
                "name": f.name,
                "address": None
            } for f in unlocated_fields_qs
        ]

        return Response({
            "located_fields": located_fields,
            "unlocated_fields": unlocated_fields,
        })

    def put(self, request, region_name, district_name):
        field_id = request.data.get('field')
        address = request.data.get('address', '')

        region = get_object_or_404(Region, name__iexact=region_name)
        district = get_object_or_404(District, name__iexact=district_name, region=region)
        field = get_object_or_404(Field, pk=field_id)

        self.check_object_permissions(request, field)

        existing_location = FieldLocation.objects.filter(field=field).exclude(district=district).first()
        if existing_location:
            return Response(
                {"error": f"Field allaqachon '{existing_location.district.name}' tumanga joylashtirilgan"},
                status=status.HTTP_400_BAD_REQUEST
            )

        FieldLocation.objects.update_or_create(
            field=field,
            district=district,
            defaults={"address": address}
        )

        return Response({"message": "Field joylashtirildi"}, status=status.HTTP_200_OK)

    def delete(self, request, region_name, district_name):
        field_id = request.data.get('field')

        region = get_object_or_404(Region, name__iexact=region_name)
        district = get_object_or_404(District, name__iexact=district_name, region=region)
        field = get_object_or_404(Field, pk=field_id)

        self.check_object_permissions(request, field)

        location_qs = FieldLocation.objects.filter(field=field, district=district)
        if not location_qs.exists():
            return Response(
                {"error": "Bu field ushbu tumanga biriktirilmagan"},
                status=status.HTTP_400_BAD_REQUEST
            )

        location_qs.delete()
        return Response({"message": "Field lokatsiyadan olib tashlandi"}, status=status.HTTP_200_OK)

class FieldViewSet(ModelViewSet):
    serializer_class = FieldSerializer  # Agar yaratishda boshqa serializer bo‘lsa, quyida handle qilamiz
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = FieldFilter
    search_fields = ['name']

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Field.objects.all()
        return Field.objects.filter(owner=user)

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return FieldCreateSerializer
        return FieldSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class AllLocatedFieldsView(APIView):
    def get(self, request):
        located_fields = Field.objects.filter(locations__isnull=False).distinct()

        result = []
        for field in located_fields:
            # Har bir field uchun barcha lokatsiyalarni olib chiqamiz
            for location in field.locations.all():
                result.append({
                    "field_id": field.id,
                    "field_name": field.name,
                    "region": location.district.region.name,
                    "district": location.district.name,
                    "address": location.address
                })

        return Response(result, status=200)

class FieldLikeViewSet(ModelViewSet):
    queryset = FieldLike.objects.all()
    serializer_class = FieldLikeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FieldLike.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        user = self.request.user
        field = serializer.validated_data['field']
        if FieldLike.objects.filter(user=user, field=field).exists():
            raise ValidationError("Siz bu maydonni allaqachon like qilgansiz.")
        serializer.save(user=user)

class FieldStatusView(generics.ListAPIView):
    queryset = Field.objects.annotate(
        likes_count=Count('likes', distinct=True),
        comments_count=Count('comments', distinct=True),
        average_rating=Avg('stars__rating')
    )
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = FieldStatusFilter

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        data = [
            {
                "id": f.id,
                "name": f.name,
                "likes_count": f.likes_count,
                "comments_count": f.comments_count,
                "average_rating": round(f.average_rating or 0, 1)
            }
            for f in queryset
        ]
        return Response(data)

class FieldCommentViewSet(ModelViewSet):
    queryset = FieldComment.objects.all()
    serializer_class = FieldCommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class FieldStarViewSet(ModelViewSet):
    queryset = FieldStar.objects.all()
    serializer_class = FieldStarSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


