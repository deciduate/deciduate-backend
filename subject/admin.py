from django.contrib import admin
from .models import Subject, ClassOf, MajorCompulsory, LiberalCompulsory

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'area', 'grade', 'credit']
    list_filter = ['area', 'grade']
    search_fields = ['name']
    list_display_links = ['name']

@admin.register(ClassOf)
class ClassOfAdmin(admin.ModelAdmin):
    list_display = ['id', 'year']

@admin.register(MajorCompulsory)
class MajorCompulsoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'subject_name', 'major', 'main_compulsory', 'sub_compulsory', 'class_of']
    list_filter = ['major', 'main_compulsory', 'sub_compulsory']
    search_fields = ['subject__name']

    def subject_name(self, obj):
        return obj.subject.name
    subject_name.short_description = '과목명'

@admin.register(LiberalCompulsory)
class LiberalCompulsoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'subject_name', 'category', 'compulsory', 'class_of']
    list_filter = ['category', 'compulsory']
    search_fields = ['subject__name']
    
    def subject_name(self, obj):
        return obj.subject.name
    subject_name.short_description = '과목명'