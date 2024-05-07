from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
from django.db import models

from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


class Subject(models.Model):
    class AreaChoices(models.TextChoices):
        MAJOR = 'M', _('전공')
        LIBERAL = 'L', _('교양')

    area = models.CharField(verbose_name='개설영역', max_length=2, choices=AreaChoices)
    grade = models.IntegerField(verbose_name='학년')
    code = models.CharField(verbose_name='학수번호', max_length=11)
    name = models.CharField(verbose_name='과목명', max_length=30)
    professor = models.CharField(verbose_name='교수', max_length=30)
    credit = models.IntegerField(verbose_name='학점')

    class Meta:
        db_table = 'subject'


class MajorCompulsory(Subject):
    main_compulsory = models.BooleanField(verbose_name='본전공 필수')
    sub_compulsory = models.BooleanField(verbose_name='이중/부전공 필수')

    class Meta:
        db_table = 'major_compulsory'


class LiberalCompulsory(Subject):
    compulsory = models.BooleanField(verbose_name='교양 필수')

    class Meta:
        db_table = 'liberal_compulsory'


class Grade(models.Model):
    from django.db import models

    class YearChoices(models.IntegerChoices):
        YEAR_18 = 18, '18'
        YEAR_19 = 19, '19'
        YEAR_20 = 20, '20'
        YEAR_21 = 21, '21'
        YEAR_22 = 22, '22'
        YEAR_23 = 23, '23'
        YEAR_24 = 24, '24'

    
    year = models.IntegerField(verbose_name='학년', choices=YearChoices)
    major_compulsory = models.ForeignKey(MajorCompulsory, verbose_name='전공 필수', on_delete=models.CASCADE, related_name='grades')
    liberal_compulsory = models.ForeignKey(LiberalCompulsory, verbose_name='교양 필수', on_delete=models.CASCADE, related_name='grades')
    
    class Meta:
        db_table = 'grade'


class Major(models.Model):
    class CampusChoices(models.TextChoices):
        SEOUL = 'S', _('서울')
        GLOBAL = 'G', _('글로벌')

    name = models.CharField(verbose_name='전공명', max_length=30, unique=True)
    campus = models.CharField(verbose_name='캠퍼스', max_length=1, choices=CampusChoices.choices)
    college = models.CharField(verbose_name='단과대학', max_length=30, null=False)

    class Meta:
        db_table = 'major'


class UserManager(BaseUserManager):
    
    use_in_migrations = True
    
    def create_user(self, email, nickname, password=None, **kwargs):
        
        if not email:
            raise ValueError('must have user email')
        user = self.model(
            email = self.normalize_email(email),
            nickname = nickname,
            password=password,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
      
    def create_superuser(self, email, nickname, password, **extra_fields):        
       
        user = self.create_user(
            email = self.normalize_email(email),
            nickname = nickname,
            password=password,
        )
        user.is_admin = True
        user.is_superuser = True    
        user.is_staff = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser,PermissionsMixin):    
    objects = UserManager()

    class TypeChoices(models.IntegerChoices):
        TYPE1 = 1, _('전공심화')
        TYPE2 = 2, _('이중전공')
        TYPE3 = 3, _('부전공')
        TYPE4 = 4, _('전공심화+부전공')
    
    email = models.EmailField(verbose_name='이메일', max_length=255, unique=True)    
    nickname = models.CharField(verbose_name='닉네임', max_length=20, unique=True)
    student_no = models.CharField(verbose_name='학번', max_length=10, unique=True, null=True)
    major_type = models.IntegerField(verbose_name='전공유형', choices=TypeChoices, default=TypeChoices.TYPE1)
    transfer = models.BooleanField(verbose_name='편입생', blank=True, default=False)
    foreign = models.BooleanField(verbose_name='외국인전형', blank=True, default=False)
    main_major = models.ForeignKey(Major, verbose_name='본전공', on_delete=models.SET_NULL, related_name='users_main', null=True)
    double_major = models.ForeignKey(Major, verbose_name='이중전공', on_delete=models.SET_NULL, related_name='users_double', null=True)
    minor_major = models.ForeignKey(Major, verbose_name='부전공', on_delete=models.SET_NULL, related_name='users_minor', null=True)

    is_active = models.BooleanField(default=True)    
    is_admin = models.BooleanField(default=False)    
    is_superuser = models.BooleanField(default=False)    
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(verbose_name='생성일', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='수정일', auto_now=True)
    USERNAME_FIELD = 'nickname'
    REQUIRED_FIELDS = ['email']

    def validate_major_null(self, *args, **kwargs):
        if not self.main_major:
            raise ValidationError("본전공 입력은 필수입니다.")
        if self.major_type == self.TypeChoices.TYPE2 and not self.double_major:
            raise ValidationError("이중전공 입력은 필수입니다.")
        if self.major_type in (self.TypeChoices.TYPE3, self.TypeChoices.TYPE4) and not self.minor_major:
            raise ValidationError("부전공 입력은 필수입니다.")
        super(MyUser, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.email

    class Meta:
        db_table = "user"