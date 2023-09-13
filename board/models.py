import datetime
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from .managers import CustomUserManager
from django.core.validators import MinLengthValidator, RegexValidator

alphanumeric_validator = RegexValidator(
    regex=r'^[a-zA-Z0-9]+$',
    message='영어, 숫자 조합만 가능합니다.',
    code='invalid_alphanumeric'
)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    user_id = models.CharField(max_length=15, validators=[MinLengthValidator(3), alphanumeric_validator], unique=True)
    profile_image = models.ImageField(upload_to='profile_image', null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    USERNAME_FIELD = "user_id"

    objects = CustomUserManager()

    class Meta:
        db_table = 'users'
        verbose_name_plural = 'users'

    def __str__(self):
        return self.user_id


class Post(models.Model):
    title = models.CharField(max_length=50, validators=[MinLengthValidator(2)])
    content = models.TextField(max_length=1000, validators=[MinLengthValidator(2)])
    writer = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'posts'

    def __str__(self):
        return self.title

    def was_published_recently(self):
        return timezone.now() - datetime.timedelta(days=1) <= self.created_at

    def was_published_this_year(self):
        return self.created_at.year == timezone.now().year

    def count_post_like(self):
        return PostLike.objects.filter(post=self).count()

    def get_comment(self):
        return Comment.objects.filter(post=self, is_active=True).order_by('-created_at')


class PostLike(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'post_like'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    content = models.TextField(max_length=1000, validators=[MinLengthValidator(1)])
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'comments'

    def was_published_recently(self):
        return timezone.now() - datetime.timedelta(days=1) <= self.created_at

    def was_published_this_year(self):
        return self.created_at.year == timezone.now().year
