from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import *

class Basic(models.Model):
    class TypeChoices(models.IntegerChoices):
        TYPE1 = 1, _('전공심화')
        TYPE2 = 2, _('이중전공')
        TYPE3 = 3, _('부전공')
        TYPE4 = 4, _('전공심화+부전공')

    user_id = models.ForeignKey(MyUser, on_delete=models.CASCADE, null=True)
    student_no = models.CharField(verbose_name='학번', max_length=10, unique=True, null=True)
    major_type = models.IntegerField(verbose_name='전공유형', choices=TypeChoices.choices, default=TypeChoices.TYPE1)
    transfer = models.BooleanField(verbose_name='편입생', blank=True, default=False)
    foreign = models.BooleanField(verbose_name='외국인전형', blank=True, default=False)
    main_major = models.ForeignKey(Major, verbose_name='본전공', on_delete=models.SET_NULL, related_name='users_main', null=True)
    double_major = models.ForeignKey(Major, verbose_name='이중전공', on_delete=models.SET_NULL, related_name='users_double', null=True)
    minor_major = models.ForeignKey(Major, verbose_name='부전공', on_delete=models.SET_NULL, related_name='users_minor', null=True)


class Credit(models.Model):
    main_major = models.IntegerField(null=True)
    double_major = models.IntegerField(null=True)
    second_major = models.IntegerField(null=True)
    outside = models.IntegerField(null=True)
    liberal = models.IntegerField(null=True)
    minor_major = models.IntegerField(null=True)
    teaching = models.IntegerField(null=True)
    self_selection = models.IntegerField(null=True)
    total_credit = models.IntegerField(null=True)
    total_score = models.FloatField(null=True)
    user_id = models.ForeignKey(MyUser, on_delete=models.CASCADE, null=True)

# 전공필수과목
class MajorCompulsorySubject(models.Model):
    status = models.BooleanField(null=True)
    subject = models.ForeignKey(MajorCompulsory, on_delete=models.CASCADE, null=True)
    user_id = models.ForeignKey(MyUser, on_delete=models.CASCADE, null=True)

# 교양필수과목
class LiberalCompulsorySubject(models.Model):
    status = models.BooleanField(null=True)
    subject = models.ForeignKey(LiberalCompulsory, on_delete=models.CASCADE, null=True)
    user_id = models.ForeignKey(MyUser, on_delete=models.CASCADE, null=True)

class Extra(models.Model):
    main_test_pass = models.BooleanField(null=True)
    double_test_pass = models.BooleanField(null=True)
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

    foreign_pass = models.IntegerField(choices = ForeignPass.choices, null=True)
    user_id = models.ForeignKey(MyUser, on_delete=models.CASCADE, null=True)