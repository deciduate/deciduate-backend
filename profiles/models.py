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
    self_selction = models.IntegerField(default=0)
    total_credit = models.IntegerField(default=0)
    total_score = models.FloatField(default=0)
    main_test_pass = models.BooleanField(default=False)
    double_test_pass = models.BooleanField(default=False)

    # 외국어 인증 시험에 따라 숫자 지정
    class ForeignPass(models.IntegerChoices):
        NONE = 1, 'None'
        FLEX = 2, 'FLEX'
        FLEX_SPEAKING = 3, 'FLEX Speaking'
        TOEIC = 4, 'TOEIC'
        TOEIC_SPEAKING = 5, 'TOEIC Speaking'
        TOEFL = 6, 'TOEFL'
        IELTS = 7, 'IELTS'
        OPIC = 8, 'OPIc'
        REPLACEMENT = 9, 'Foreign Language Certification Replacement'
        # 외국어 인증 대체 과정

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
