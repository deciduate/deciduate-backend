from django.contrib import admin
from .models import Requirement

@admin.register(Requirement)
class RequirementAdmin(admin.ModelAdmin):
    list_display = ('id', 'major_id', 'student_no', 'major_type',)

    def major_name(self, obj):
        return obj.major_id.name if obj.major_id else None

    major_name.short_description = '전공명'
