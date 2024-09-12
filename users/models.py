from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import (EmailValidator, FileExtensionValidator, 
                                    MaxLengthValidator, MinLengthValidator)
from django.db import models

from services import get_path_upload_avatar, validate_avatar


class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True, validators=[UnicodeUsernameValidator()],)
    email = models.EmailField(max_length=150, unique=True, validators=[
        EmailValidator(message="Введите корректный email адрес."),
        MinLengthValidator(6, message="Email должен содержать минимум 6 символов."),
        MaxLengthValidator(150, message="Email должен быть не длиннее 150 символов."),
    ])
    date_joined = models.DateTimeField(default=timezone.now)
    avatar = models.ImageField(upload_to=get_path_upload_avatar, 
                               blank=True, 
                               null=True, 
                               validators=[FileExtensionValidator(allowed_extensions=["jpg", "jpeg"]), 
                                           validate_avatar])


    USERNAME_FIELD = "username"

    class Meta:
        db_table = "users"
        verbose_name = "Пользователя"
        verbose_name_plural = "Пользователи"
        ordering = ['id']


    def __str__(self):
        return self.username
    
    