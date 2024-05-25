from django.db import models
from django.utils.translation import gettext_lazy as _

from major.models import Major

class Subject(models.Model):
    class AreaChoices(models.TextChoices):
        MAJOR = 'M', _('전공')
        LIBERAL = 'L', _('교양')

    area = models.CharField(verbose_name='개설영역', max_length=2, choices=AreaChoices.choices)
    grade = models.IntegerField(verbose_name='학년', null=True)
    name = models.CharField(verbose_name='과목명', max_length=100)
    credit = models.IntegerField(verbose_name='학점')

    class Meta:
        db_table = 'subject'


class ClassOf(models.Model):
    year = models.IntegerField(verbose_name='학년')
    
    class Meta:
        db_table = 'class_of'


class MajorCompulsory(models.Model):
    subject = models.ForeignKey(Subject, verbose_name='과목', related_name='subject_major_compulsory', on_delete=models.CASCADE)
    major = models.ForeignKey(Major, verbose_name='전공', related_name='major', on_delete=models.SET_NULL, null=True)
    main_compulsory = models.BooleanField(verbose_name='본전공 필수', default=True)
    sub_compulsory = models.BooleanField(verbose_name='이중/부전공 필수', default=True)
    class_of = models.ForeignKey(ClassOf, verbose_name='학번', related_name='class_of_major_compulsories', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'major_compulsory'


class LiberalCompulsory(models.Model):
    subject = models.ForeignKey(Subject, verbose_name='과목', related_name='subject_liberal_compulsory', on_delete=models.CASCADE)
    category = models.CharField(verbose_name='교양 영역', max_length=20, null=True)
    compulsory = models.BooleanField(verbose_name='교양 필수', default=True)
    class_of = models.ForeignKey(ClassOf, verbose_name='학번', related_name='class_of_liberal_compulsories', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'liberal_compulsory'