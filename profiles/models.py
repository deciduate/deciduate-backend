from django.db import models
from django.utils.translation import gettext_lazy as _

from major.models import Major

# 프로필
class Profile(models.Model):
    main_major = models.IntegerField(default=0)
    double_major = models.IntegerField(default=0)
    second_major = models.IntegerField(default=0)
    outside = models.IntegerField(default=0)
    liberal = models.IntegerField(default=0)
    minor_major = models.IntegerField(default=0)
    teaching = models.IntegerField(default=0)
    self_selection = models.IntegerField(default=0)
    total_credit = models.IntegerField(default=0)
    total_score = models.FloatField(default=0)
    main_test_pass = models.BooleanField(default=False)
    double_test_pass = models.BooleanField(default=False)

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

    foreign_pass = models.IntegerField(choices = ForeignPass.choices, default = ForeignPass.NONE)

class Basic(models.Model):
    class TypeChoices(models.IntegerChoices):
        TYPE1 = 1, _('전공심화')
        TYPE2 = 2, _('이중전공')
        TYPE3 = 3, _('부전공')
        TYPE4 = 4, _('전공심화+부전공')

    nickname = models.CharField(verbose_name='닉네임', max_length=20, unique=True)
    student_no = models.CharField(verbose_name='학번', max_length=10, unique=True, null=True)
    major_type = models.IntegerField(verbose_name='전공유형', choices=TypeChoices.choices, default=TypeChoices.TYPE1)
    transfer = models.BooleanField(verbose_name='편입생', blank=True, default=False)
    foreign = models.BooleanField(verbose_name='외국인전형', blank=True, default=False)
    main_major = models.ForeignKey(Major, verbose_name='본전공', related_name='users_main', on_delete=models.SET_NULL, null=True)
    double_major = models.ForeignKey(Major, verbose_name='이중전공', related_name='users_double', on_delete=models.SET_NULL, null=True)
    minor_major = models.ForeignKey(Major, verbose_name='부전공', related_name='users_minor', on_delete=models.SET_NULL, null=True)


class CompulsorySubject(models.Model):
    status = models.BooleanField(default=False)
