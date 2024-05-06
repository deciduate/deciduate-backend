from django.db import models

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
    total_score = models.IntegerField(default=0)
    main_test_pass = models.BooleanField(default=False)
    double_test_pass = models.BooleanField(default=False)

    # 외국어 인증 시험에 따라 숫자 지정
    class Foreign_pass(models.IntegerChoices):
        NONE = 1
        FLEX = 2
        FLEX_SPEAKING = 3
        TOEIC = 4
        TOEIC_SPEAKING = 5
        TOEFL = 6
        IELTS = 7
        OPIc = 8
        REPLACEMENT = 9 # 외국어 인증 대체 과정

    foreign_pass = models.IntegerField(
        choices = Foreign_pass.choices,
        default = Foreign_pass.NONE
    )
    user_id = models.ForeignKey("User", related_name="user", on_delete=models.CASCADE, db_column="user_id")
    
class Compulsory_Subject(models.Model):
    profile_id = models.ForeignKey("Profile", related_name="profile", on_delete=models.CASCADE, db_column="profile_id")
    status = models.BooleanField()
    subject_id = models.ForeignKey("Subject", related_name="subject", on_delete=models.CASCADE, db_column="subject_id")