# Generated by Django 5.1.1 on 2024-09-15 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_alter_comment_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
