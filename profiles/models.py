from django.db import models

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