from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


class UserManager(BaseUserManager):
    
    use_in_migrations = True
    
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('이메일은 필수입니다.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()  # 비밀번호를 설정하지 않을 경우
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_admin') is not True:
            raise ValueError('슈퍼유저는 is_admin=True로 설정되어야 합니다.')
        return self.create_user(email, password, **extra_fields)


class MyUser(AbstractBaseUser,PermissionsMixin):    
    objects = UserManager()
    
    email = models.EmailField(verbose_name='이메일', max_length=100, unique=True)
    
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
