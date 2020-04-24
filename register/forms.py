from django.contrib.auth.forms import (
    UserCreationForm, PasswordChangeForm,
    PasswordResetForm, SetPasswordForm,
    AuthenticationForm,
)
from django.contrib.auth import get_user_model, authenticate
from django import forms
from django.utils.text import capfirst

User = get_user_model()

class LoginForm(AuthenticationForm):
    """ ログインフォーム """

    error_messages = {
        'invalid_login': ("5回連続でログインに失敗すると安全のためアカウントを一時的にロック致します。"
                           "ご了承ください"),
        'inactive': ("This account is inactive."),
    }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label

class UserCreateForm(UserCreationForm):
    """ ユーザー登録用フォーム """
    class Meta:
        model = User
        fields = ('email',)
        

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    # 仮登録段階でアカウントを一度削除
    def clean_email(self):
        email = self.cleaned_data['email']
        User.objects.filter(email=email, is_active=False).delete()
        return email

class MyPasswordChangeForm(PasswordChangeForm):
    """ パスワード変更フォーム """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class EmailChangeForm(forms.ModelForm):
    """ メールアドレス変更フォーム """
    class Meta:
        model = User
        fields = ('email',)
        

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    # 仮登録段階でアカウントを一度削除
    def clean_email(self):
        email = self.cleaned_data['email']
        User.objects.filter(email=email, is_active=False).delete()
        return email

class MyPasswordResetForm(PasswordResetForm):
    """パスワード忘れたときのフォーム"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class MySetPasswordForm(SetPasswordForm):
    """パスワード再設定用フォーム(パスワード忘れて再設定)"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'