from django.contrib import admin
from .models import Bron, Game


@admin.register(Bron)
class BronAdmin(admin.ModelAdmin):
    list_display = ('user', 'field', 'situation', 'date', 'bron_created_at')
    list_filter = ('situation', 'date', 'field')
    search_fields = ('user__username', 'field__name')
    ordering = ('-date',)


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('bron', 'started_at', 'completed_at', 'price_per_hour')
    search_fields = ('bron__user__username', 'bron__field__name')
    list_filter = ('started_at', 'completed_at')



