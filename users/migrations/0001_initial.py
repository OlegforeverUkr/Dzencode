# Generated by Django 5.1.1 on 2024-09-11 12:49

import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
import django.utils.timezone
import services
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('username', models.CharField(max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()])),
                ('email', models.EmailField(max_length=150, unique=True, validators=[django.core.validators.EmailValidator(message='Введите корректный email адрес.'), django.core.validators.MinLengthValidator(6, message='Email должен содержать минимум 6 символов.'), django.core.validators.MaxLengthValidator(150, message='Email должен быть не длиннее 150 символов.')])),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('avatar', models.ImageField(blank=True, null=True, upload_to=services.get_path_upload_avatar, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg']), services.validate_avatar])),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Пользователя',
                'verbose_name_plural': 'Пользователи',
                'db_table': 'users',
                'ordering': ['id'],
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
