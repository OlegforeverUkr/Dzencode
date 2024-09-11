from django import forms
from django.core.exceptions import ValidationError
from PIL import Image
from .models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'avatar']

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')

        if avatar:
            img = Image.open(avatar)

            max_width, max_height = 320, 240
            
            if img.width > max_width or img.height > max_height:
                img.thumbnail((max_width, max_height), Image.ANTIALIAS)
                img_temp_path = avatar.temporary_file_path()
                img.save(img_temp_path)

        return avatar
