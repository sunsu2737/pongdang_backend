from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.


class UserManager(BaseUserManager):

    use_in_migrations = True

    def create_user(self, email, nickname, password=None):

        if not email:
            raise ValueError('must have user email')
        user = self.model(
            email=self.normalize_email(email),
            nickname=nickname
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, nickname='admin'):

        user = self.create_user(
            email=self.normalize_email(email),
            nickname=nickname,
            password=password
        )
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    '''
        # 필수
        이메일 -> 로그인, 인증
        닉네임 -> 표시이름

        # 선택
        프로필 이미지-> 미디어 경로
        이름 -> 본명
        생년월일 -> 생년월일

        # 보류
        지역 -> 지역번호?
    '''
    email = models.EmailField(verbose_name="email", unique=True)
    nickname = models.CharField(max_length=24, unique=True)
    auth = models.BooleanField(default=False)
    profile_image = models.TextField(default='default_image')
    name = models.CharField(max_length=10, default='')
    birth = models.TextField(default='')
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'email'

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    def __str__(self):
        return f"{self.nickname} : {self.email}"

    class Meta:
        db_table = 'User'


class Feed(models.Model):
    post = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="post/%Y/%m/%d")
