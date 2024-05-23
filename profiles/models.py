from django.db import models
from django.utils.translation import gettext_lazy as _

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

    foreign_pass = models.IntegerField(choices = ForeignPass.choices, default = ForeignPass.TYPE1)

class CompulsorySubject(models.Model):
    status = models.BooleanField(default=False)