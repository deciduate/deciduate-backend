from django.contrib import admin
from .models import MyUser

from django.contrib import admin

@admin.register(MyUser)
class UserAdmin(admin.ModelAdmin):

    list_display = (
        'email',
<<<<<<< HEAD
        'created_at',
        'updated_at',
=======
        'nickname',
        'created_at',
>>>>>>> 9c807d7 (Feat: User 모델 설계)
    )

    list_display_links = (
        'email',
    )