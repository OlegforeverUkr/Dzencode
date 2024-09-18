import bleach
from django import forms
from django.core.validators import RegexValidator, EmailValidator, URLValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from captcha.fields import CaptchaField

from posts.models import Comment, Post
from services import validate_size_upload_textfile, validate_upload_comments_images


ALLOWED_TAGS = ['a', 'code', 'i', 'strong']
ALLOWED_ATTRIBUTES = {'a': ['href', 'title']}


class AddCommentForm(forms.ModelForm):
    parent_id = forms.IntegerField(widget=forms.HiddenInput(), required=False)

    user_name = forms.CharField(
        widget=forms.TextInput(
            attrs={'autofocus': True,
                   'placeholder': 'Введите ваше имя',
                   'class': 'form-control'}),
        label='User Name',
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z0-9]+$',
                message=_('User name can only contain letters and numbers.')
            )
        ]
    )

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={'placeholder': 'Введите ваш email',
                   'class': 'form-control'}),
        label='E-mail',
        validators=[EmailValidator()]
    )

    home_page = forms.URLField(
        widget=forms.URLInput(
            attrs={'placeholder': 'Введите вашу страничку',
                   'class': 'form-control'}),
        label='Home Page',
        required=False,
        validators=[URLValidator()]
    )

    image = forms.ImageField(required=False)
    file = forms.FileField(required=False)

    captcha = CaptchaField()

    text = forms.CharField(
        label='Text',
        widget=forms.Textarea(
            attrs={'rows': 4, 'cols': 40, 'class': 'form-control', 'id': 'id_body'}),
        help_text=_('You can use the following HTML tags: a, i, strong, code.')
    )

    class Meta:
        model = Comment
        fields = ['user_name', 'email', 'home_page', 'captcha', 'text', 'parent_id']



    def clean(self):
        cleaned_data = super().clean()

        user = self.initial['user']

        if not user.is_authenticated:
            raise ValidationError(_('Вы должны войти в систему, чтобы оставлять комментарии.'))

        entered_username = cleaned_data.get('user_name')
        entered_email = cleaned_data.get('email')


        if entered_username != user.username:
            raise ValidationError(_('Введённое имя пользователя не соответствует текущему пользователю.'))
        if entered_email != user.email:
            raise ValidationError(_('Введённый email не соответствует текущему пользователю.'))

        image = cleaned_data.get('image')
        if image:
            validate_upload_comments_images(image)

        file = cleaned_data.get('file')
        if file:
            validate_size_upload_textfile(file)

        return cleaned_data


class AddPostForm(forms.ModelForm):
    user_name = forms.CharField(
        widget=forms.TextInput(
            attrs={'autofocus': True,
                   'placeholder': 'Введите ваше имя',
                   'class': 'form-control'}),
        label='User Name',
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z0-9]+$',
                message=_('User name can only contain letters and numbers.')
            )
        ]
    )

    title = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder': 'Название поста',
                   'class': 'form-control'}),
        label='Title'
    )

    body = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 4, 'cols': 40, 'class': 'form-control', 'id': 'id_body'}),
        label='Text',
        help_text=_('You can use the following HTML tags: a, i, strong, code.')
    )

    url = forms.URLField(
        widget=forms.URLInput(
            attrs={'placeholder': 'Введите вашу страничку',
                   'class': 'form-control'}),
        label='Home Page',
        required=False,
        validators=[URLValidator()])

    class Meta:
        model = Post
        fields = ['user_name', 'title', 'body', 'url']

    def clean_body(self):
        body = self.cleaned_data.get('body')

        allowed_tags = ['a', 'i', 'strong', 'code']
        cleaned_body = bleach.clean(body, tags=allowed_tags, strip=False)

        if body != cleaned_body:
            raise ValidationError(_('Текст содержит запрещенные HTML-теги или некорректные атрибуты.'))

        return cleaned_body

    def clean(self):
        cleaned_data = super().clean()

        user = self.initial['user']
        if not user.is_authenticated:
            raise ValidationError(_('Вы должны войти в систему, чтобы оставлять комментарии.'))

        entered_username = cleaned_data.get('user_name')
        if entered_username != user.username:
            raise ValidationError(_('Введённое имя пользователя не соответствует текущему пользователю.'))

        return cleaned_data