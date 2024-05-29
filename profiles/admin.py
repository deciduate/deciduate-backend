from django.contrib import admin
from .models import Basic, Credit, UserMajorCompulsory, UserLiberalCompulsory, Extra

@admin.register(Basic)
class BasicAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'student_no', 'major_type', 'transfer', 'foreign_st', 'get_main_major_name', 'get_double_major_name', 'get_minor_major_name')
    list_display_links = ('id', 'user_id')

    def get_main_major_name(self, obj):
        return obj.main_major.name if obj.main_major else None
    def get_double_major_name(self, obj):
        return obj.double_major.name if obj.double_major else None
    def get_minor_major_name(self, obj):
        return obj.minor_major.name if obj.minor_major else None

    get_main_major_name.short_description = '본전공'
    get_double_major_name.short_description = '이중전공'
    get_minor_major_name.short_description = '부전공'

@admin.register(Credit)
class CreditAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'main_major_credit', 'double_major_credit', 'second_major_credit', 'outside_credit', 'liberal_credit', 'minor_major_credit', 'teaching_credit', 'self_selection_credit', 'total_credit', 'total_score')
    list_display_links = ('id', 'user_id')

@admin.register(UserMajorCompulsory)
class UserMajorCompulsoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'status', 'get_subject_name')
    list_display_links = ('id', 'user_id')

    def get_subject_name(self, obj):
        return obj.subject.name if obj.subject else None
    get_subject_name.short_description = '과목명'

@admin.register(UserLiberalCompulsory)
class UserLiberalCompulsoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'status', 'get_subject_name')
    list_display_links = ('id', 'user_id')

    def get_subject_name(self, obj):
        return obj.subject.name if obj.subject else None
    get_subject_name.short_description = '과목명'
    

@admin.register(Extra)
class ExtraAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'main_test_pass', 'double_test_pass', 'foreign_certification')
    list_display_links = ('id', 'user_id')
