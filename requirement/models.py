from django.db import models
from major.models import *

# Create your models here.
class Requirement(models.Model):
    major_id = models.ForeignKey(Major, null=True, on_delete=models.SET_NULL)
    student_no = models.CharField(max_length=2)
    major_type = models.IntegerField(default=1)

    main_major = models.IntegerField(default=0)
    double_major = models.IntegerField(default=0)
    minor_major  = models.IntegerField(default=0)
    liberal = models.IntegerField(default=0)
    practical_foreign = models.IntegerField(default=0) #실용외국어
    self_selection = models.IntegerField(default=0)
    total_credit = models.IntegerField(default=0)
    test_type = models.CharField(max_length=10)
    flex = models.IntegerField(default=0) 
    flex_speaking = models.IntegerField(default=0) 
    toeic = models.IntegerField(default=0) 
    toeic_speaking = models.IntegerField(default=0) 

    # OPIc_grade = [
    #     ('AL', 'Advanced Low'),
    #     ('IH', 'Intermediate High'),
    #     ('IM1', 'Intermediate Mid 1'),
    #     ('IM2', 'Intermediate Mid 2'),
    #     ('IM3', 'Intermediate Mid 3'),
    #     ('IL', 'Intermediate Low'),
    #     ('NH', 'Novice High'),
    #     ('NM', 'Novice Mid'),
    #     ('NL', 'Novice Low'),
    # ]
    opic = models.CharField(max_length=5) #choices=OPIc_grade ?
    
    class Meta:
        unique_together = ('major_id', 'student_no', 'major_type')
    