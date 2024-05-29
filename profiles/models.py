from django.db import models
from django.utils.translation import gettext_lazy as _

from major.models import Major
from users.models import MyUser

from subject.models import MajorCompulsory, LiberalCompulsory

class Basic(models.Model):
    class TypeChoices(models.IntegerChoices):
        TYPE1 = 1, _('전공심화')
        TYPE2 = 2, _('이중전공')
        TYPE3 = 3, _('부전공')
        TYPE4 = 4, _('전공심화+부전공')

    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    student_no = models.IntegerField(verbose_name='학번', blank=True, null=True)
    major_type = models.IntegerField(verbose_name='전공유형', choices=TypeChoices.choices, default=TypeChoices.TYPE1)
    transfer = models.BooleanField(verbose_name='편입생', blank=True, null=True)
    foreign_st = models.BooleanField(verbose_name='외국인전형', blank=True, null=True)
    main_major = models.ForeignKey(Major, verbose_name='본전공', on_delete=models.SET_NULL, related_name='users_main', blank=True, null=True)
    double_major = models.ForeignKey(Major, verbose_name='이중전공', on_delete=models.SET_NULL, related_name='users_double', blank=True, null=True)
    minor_major = models.ForeignKey(Major, verbose_name='부전공', on_delete=models.SET_NULL, related_name='users_minor', blank=True, null=True)

class Credit(models.Model):
    main_major_credit = models.IntegerField(verbose_name='1전공', blank=True, null=True)
    double_major_credit = models.IntegerField(verbose_name='이중전공', blank=True, null=True)
    second_major_credit = models.IntegerField(verbose_name='2전공', blank=True, null=True)
    outside_credit = models.IntegerField(verbose_name='실외', blank=True, null=True)
    liberal_credit = models.IntegerField(verbose_name='교양', blank=True, null=True)
    minor_major_credit = models.IntegerField(verbose_name='부전공', blank=True, null=True)
    teaching_credit = models.IntegerField(verbose_name='교직', blank=True, null=True)
    self_selection_credit = models.IntegerField(verbose_name='자선', blank=True, null=True)
    total_credit = models.IntegerField(verbose_name='총취득', blank=True, null=True)
    total_score = models.FloatField(verbose_name='총평점', blank=True, null=True)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)

# 전공필수과목
class UserMajorCompulsory(models.Model):
    status = models.BooleanField(verbose_name='상태', blank=True, null=True)
    subject = models.ForeignKey(MajorCompulsory, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)

# 교양필수과목
class UserLiberalCompulsory(models.Model):
    status = models.BooleanField(verbose_name='상태', blank=True, null=True)
    subject = models.ForeignKey(LiberalCompulsory, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)

class Extra(models.Model):
    main_test_pass = models.BooleanField(verbose_name='본전공 통과', blank=True, null=True)
    double_test_pass = models.BooleanField(verbose_name='이중전공 통과', blank=True, null=True)
    # 외국어 인증 시험에 따라 숫자 지정
    class ForeignPass(models.IntegerChoices):
        TYPE1 = 1, _('해당없음')
        TYPE2 = 2, _('FLEX')
        TYPE3 = 3, _('FLEX 스피킹')
        TYPE4 = 4, _('TOEIC')
        TYPE5 = 5, _('TOEIC 스피킹')
        TYPE6 = 6, _('TOEFL')
        TYPE7 = 7, _('IELTS')
        TYPE8 = 8, _('OPIc')
        TYPE9 = 9, _('외국어인증대체과정')

    foreign_certification = models.IntegerField(verbose_name='외국어인증', choices = ForeignPass.choices, blank=True, null=True)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
