from django import forms
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from CompGeek.settings import STATIC_URL, DEFAULT_ARTICLE_AVATAR
from .models import *
from .utilities import *



class TextWriteWidget(forms.TextInput):


    class Media:
        js = ("https://cdn.tiny.cloud/1/fz2mhs07b3qgkc5uyvxi3oskmyjkfqv7iteam2qivgn106v5/tinymce/5/tinymce.min.js",
              STATIC_URL + 'js/tiny_init.js?ver=1.9',)

class ArticleWriteForm(forms.ModelForm):
    text = forms.CharField(widget=TextWriteWidget(attrs={'id': 'article_text'}), required=False)

    def clean(self):
        super().clean()
        text = self.cleaned_data['text']
        if len(text) == 0:
            errors = {'text': ValidationError(
                'поле обязательно к заполенению',
                )}
            raise ValidationError(errors)

    def save(self, commit=True):
        article = super().save(commit=False)
        article.tag = transliterate(article.label)
        if not article.avatar.name:
            article.avatar.name = DEFAULT_ARTICLE_AVATAR
        if not commit:
            return article
        article.save()



    class Meta:
        model = Article
        fields = ['label', 'avatar', 'text', 'preview_text', 'primary_category', 'secondary_category']

class ArticleAdminWriteForm(forms.ModelForm):
    text = forms.CharField(widget=TextWriteWidget(attrs={'id': 'article_text'}))


    def save(self, commit=True):
        article = super().save(commit=False)
        article.tag = transliterate(article.label)
        if not article.avatar.name:
            article.avatar.name = DEFAULT_ARTICLE_AVATAR
        if not commit:
            return article
        article.save()


    class Meta:
        model = Article
        fields = ['label', 'tag', 'avatar', 'text', 'preview_text', 'primary_category', 'secondary_category', 'author']


class ChangeUserPasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput(), label='Старый пароль')
    new_password1 = forms.CharField(widget=forms.PasswordInput(), label='Новый пароль')
    new_password2 = forms.CharField(widget=forms.PasswordInput(), label='Повторите пароль')


class ChangeUserInfoForm(forms.ModelForm):
	email = forms.EmailField(required=True, label='Адрес элетронной почты')

	class Meta:
		model = User
		fields = ['username', 'avatar', 'email']

class LoginForm(forms.Form):
    username = forms.CharField(label='Имя')
    password = forms.CharField(widget=forms.PasswordInput(), label='Пароль')

class CommentForm(forms.ModelForm):
    text = forms.CharField(widget=TextWriteWidget(attrs={'id': 'comment_text'}), required=False)

    def clean(self):
        text = self.cleaned_data['text']
        if len(text) == 0:
            errors = {
                'text': ValidationError('Введите комментарии', code='text_miss')
            }
            raise ValidationError(errors)
    class Meta:
        model = Comment
        fields = ['text']

class CommentAdminForm(forms.ModelForm):
    text = forms.CharField(widget=TextWriteWidget(attrs={'id': 'comment_text'}), required=False)

    def clean(self):
        text = self.cleaned_data['text']
        if len(text) == 0:
            errors = {
                'text': ValidationError('Введите комментарии', code='text_miss')
            }
            raise ValidationError(errors)
    class Meta:
        model = Comment
        fields = ['author', 'article', 'text']


class RegisterUserForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Адрес элетронной почты')
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput, )
    password2 = forms.CharField(label='Пароль(повторно)', widget=forms.PasswordInput,
                                help_text='Введите пароль ещё раз')

    def clean_password1(self):
        password1 = self.cleaned_data['password1']
        if password1:
            password_validation.validate_password(password1)
        return password1

    def clean(self):
        super().clean()
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 and password2 and password1 != password2:
            errors = {'password2': ValidationError(
                'Введенные пароли не совпадают',
                code='password_mismatch')}
            raise ValidationError(errors)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ['username', 'avatar', 'email']

