from django.contrib import admin
from .models import Field, FieldLocation, FieldImage, FieldLike, FieldComment, FieldStar

@admin.register(Field)
class FieldAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'location', 'price_per_hour', 'created_at')
    search_fields = ('name', 'location', 'owner__username')
    list_filter = ('created_at', 'location')

@admin.register(FieldLocation)
class FieldLocationAdmin(admin.ModelAdmin):
    list_display = ('field', 'district', 'address', 'latitude', 'longitude')
    search_fields = ('field__name', 'district')

@admin.register(FieldImage)
class FieldImageAdmin(admin.ModelAdmin):
    list_display = ('field', 'image')

@admin.register(FieldLike)
class FieldLikeAdmin(admin.ModelAdmin):
    list_display = ('field', 'user')

@admin.register(FieldComment)
class FieldCommentAdmin(admin.ModelAdmin):
    list_display = ('field', 'user', 'comment', 'created_at')
    search_fields = ('user__username', 'field__name', 'comment')
    list_filter = ('created_at',)

@admin.register(FieldStar)
class FieldStarAdmin(admin.ModelAdmin):
    list_display = ('field', 'user', 'rating')
    list_filter = ('rating',)


