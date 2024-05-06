from django.contrib import admin
from .models import MyUser

from django.contrib import admin

@admin.register(MyUser)
class UserAdmin(admin.ModelAdmin):

    list_display = (
        'email',
        'created_at',
        'updated_at',
    )

    list_display_links = (
        'email',
    )