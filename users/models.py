from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from major.models import Major

class UserManager(BaseUserManager):
    
    use_in_migrations = True
    
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('must have user email')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        return self.create_user(email, password, **extra_fields)


class MyUser(AbstractBaseUser,PermissionsMixin):    
    objects = UserManager()

    class TypeChoices(models.IntegerChoices):
        TYPE1 = 1, _('전공심화')
        TYPE2 = 2, _('이중전공')
        TYPE3 = 3, _('부전공')
        TYPE4 = 4, _('전공심화+부전공')
    
    email = models.EmailField(verbose_name='이메일', max_length=100, unique=True)
    nickname = models.CharField(verbose_name='닉네임', max_length=20, unique=True)
    student_no = models.CharField(verbose_name='학번', max_length=10, unique=True, null=True)
    major_type = models.IntegerField(verbose_name='전공유형', choices=TypeChoices.choices, default=TypeChoices.TYPE1)
    transfer = models.BooleanField(verbose_name='편입생', blank=True, default=False)
    foreign = models.BooleanField(verbose_name='외국인전형', blank=True, default=False)
    main_major = models.ForeignKey(Major, verbose_name='본전공', related_name='users_main', on_delete=models.SET_NULL, null=True)
    double_major = models.ForeignKey(Major, verbose_name='이중전공', related_name='users_double', on_delete=models.SET_NULL, null=True)
    minor_major = models.ForeignKey(Major, verbose_name='부전공', related_name='users_minor', on_delete=models.SET_NULL, null=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(verbose_name='생성일', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='수정일', auto_now=True)
    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['email']

    def clean(self):
        if not self.main_major:
            raise ValidationError("본전공 입력은 필수입니다.")
        if self.major_type == self.TypeChoices.TYPE2 and not self.double_major:
            raise ValidationError("이중전공 입력은 필수입니다.")
        if self.major_type in (self.TypeChoices.TYPE3, self.TypeChoices.TYPE4) and not self.minor_major:
            raise ValidationError("부전공 입력은 필수입니다.")
        super().clean()
    
    def __str__(self):
        return self.email

    class Meta:
        db_table = "users"