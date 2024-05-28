from django.contrib import admin
from .models import Basic, Credit, MajorCompulsorySubject, LiberalCompulsorySubject, Extra

@admin.register(Basic)
class BasicAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'student_no', 'major_type', 'transfer', 'foreign', 'main_major', 'double_major', 'minor_major')
    list_display_links = ('id', 'user_id')

@admin.register(Credit)
class CreditAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'main_major', 'double_major', 'second_major', 'outside', 'liberal', 'minor_major', 'teaching', 'self_selection', 'total_credit', 'total_score')
    list_display_links = ('id', 'user_id')

@admin.register(MajorCompulsorySubject)
class MajorCompulsorySubjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'status', 'subject')
    list_display_links = ('id', 'user_id')

@admin.register(LiberalCompulsorySubject)
class LiberalCompulsorySubjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'status', 'subject')
    list_display_links = ('id', 'user_id')

@admin.register(Extra)
class ExtraAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'main_test_pass', 'double_test_pass', 'foreign_pass')
    list_display_links = ('id', 'user_id')
