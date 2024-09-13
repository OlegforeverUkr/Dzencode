from django.core.validators import FileExtensionValidator
from django.db import models
from services import (get_path_upload_comments_images, 
                      get_path_upload_textfile, 
                      validate_size_upload_textfile, 
                      validate_upload_comments_images)

from users.models import User


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=255)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        db_table = "posts"
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
        ordering = ['-created_at']


    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()
    image = models.ImageField(upload_to=get_path_upload_comments_images, null=True, blank=True)
    file = models.FileField(upload_to=get_path_upload_textfile, 
                            null=True, 
                            blank=True, 
                            validators=[
                                FileExtensionValidator(allowed_extensions=["txt"]),
                                validate_size_upload_textfile,
                            ])
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        db_table = "comments"
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ['-created_at']


    def __str__(self):
        return f"Comment by {self.user} on {self.post}"
    

    def save(self, *args, **kwargs):
        if self.image and hasattr(self.image, 'file'):
            self.image = validate_upload_comments_images(self.image.file)
        super().save(*args, **kwargs)
