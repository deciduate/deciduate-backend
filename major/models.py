from django.db import models
from django.utils.translation import gettext_lazy as _

class Major(models.Model):
    class CampusChoices(models.TextChoices):
        SEOUL = 'S', _('서울')
        GLOBAL = 'G', _('글로벌')

    name = models.CharField(verbose_name='전공명', max_length=30, unique=True)
    campus = models.CharField(verbose_name='캠퍼스', max_length=1, choices=CampusChoices.choices)
    college = models.CharField(verbose_name='단과대학', max_length=30, null=False)

    class Meta:
        db_table = 'major'