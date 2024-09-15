from django import forms
from django.core.validators import RegexValidator, EmailValidator, URLValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from captcha.fields import CaptchaField


from posts.models import Comment


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
            attrs={'rows': 4, 'cols': 40, 'class': 'form-control'}),
        help_text=_('No HTML tags allowed.')
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


        if cleaned_data.get('image'):
            validate_upload_comments_images(image)

        if cleaned_data.get('file'):
            validate_size_upload_textfile(file)

        parent_id = cleaned_data.get('parent_id')
        if parent_id is not None:
            try:
                int(parent_id)
            except ValueError:
                raise ValidationError(_('Parent ID должен быть целым числом.'))

        return cleaned_data