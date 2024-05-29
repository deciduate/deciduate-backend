from django.contrib import admin
from .models import Major

@admin.register(Major)
class MajorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'campus', 'college')
    list_display_links = ('id', 'name')
