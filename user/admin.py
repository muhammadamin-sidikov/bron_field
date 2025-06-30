from django.contrib import admin
from django.contrib.auth.models import User
from .models import UserProfile, UserLocation

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'birth_date', 'gender')
    search_fields = ('user__username', 'phone', 'gender')

class UserLocationAdmin(admin.ModelAdmin):
    list_display = ('user', 'city', 'district')
    search_fields = ('user__username', 'city', 'district')

admin.site.unregister(User)  # defaultni o'chirib
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active')
    search_fields = ('username', 'email')

admin.site.register(User, CustomUserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(UserLocation, UserLocationAdmin)
