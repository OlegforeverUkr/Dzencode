from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, UserCreationForm
from PIL import Image
from .models import User


class UserAuthForm(AuthenticationForm):

    class Meta:
        model = User
        fields = ('username', 'email', 'avatar')


    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "autofocus": True,
                "class": "form-control",
                "placeholder": "Введите ваше имя пользователя",
            }
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "current-password",
                "class": "form-control",
                "placeholder": "Введите ваш пароль",
            }
        ),
    )


class UserRegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password1",
            "password2",
        )
    
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "autofocus": True,
                "class": "form-control",
                "placeholder": "Введите ваше имя пользователя",
            }
        ))
    
    email = forms.CharField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Введите ваш email",
            }
        )
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Введите ваш пароль",
            }
        ))
    
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Повторите ваш пароль",
            }
        ))



class UserProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = (
            "avatar",
            "username",
            "email"
        )

    avatar = forms.ImageField(required=False)
    username = forms.CharField()
    email = forms.CharField()


    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')

        if avatar:
            try:
                img = Image.open(avatar)
            except Exception:
                raise ValidationError("Не удалось открыть изображение.")

            max_width = 320
            max_height = 240

            if img.width > max_width or img.height > max_height:
                raise ValidationError(
                    f"Изображение должно быть не более {max_width}x{max_height} пикселей."
                )

        return avatar

