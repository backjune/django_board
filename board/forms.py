from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, UsernameField, \
    PasswordChangeForm
from django.forms import TextInput, ModelForm, Textarea

from .models import CustomUser, Post, Comment


class CustomUserCreationForm(UserCreationForm):
    profile_image = forms.ImageField(required=False,
                                     widget=forms.ClearableFileInput(
                                         attrs={'class': 'form-control', 'id': 'inputGroupFile02'})
                                     )
    password1 = forms.CharField(
        min_length=4,
        label='',
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password",
                   'class': "form-control",
                   'id': 'floatingPassword'}),
        error_messages={
            'required': "필수 정보입니다.",
        }
    )
    password2 = None

    class Meta:
        model = CustomUser
        fields = ("user_id", "profile_image")
        widgets = {
            'user_id': TextInput(attrs={
                'class': "form-control", 'id': 'floatingInput'
            }),
        }
        error_messages = {
            'user_id': {
                'required': "필수 정보입니다.",
                'unique': "이미 등록된 아이디입니다. 다른 아이디를 입력해 주세요.",
                'max_length': "아이디는 15글자 이하만 가능합니다.",
                'min_length': "아이디는 3글자 이상만 가능합니다.",
            },
        }


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("user_id",)


class CustomUserLoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(
        attrs={"autofocus": True,
               'class': "form-control",
               'id': 'floatingInput'
               }))
    password = forms.CharField(
        min_length=4,
        label='',
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password",
                   'class': "form-control",
                   'id': 'floatingPassword'}),
        error_messages={
            'required': "필수 정보입니다.",
        }
    )

    error_messages = {
        'invalid_login': '아이디 또는 비밀번호가 올바르지 않습니다. 다시 시도해 주세요.',
    }


class CustomUserUpdateForm(PasswordChangeForm):
    old_password = forms.CharField(
        min_length=4,
        label='',
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password",
                   'class': "form-control",
                   'id': 'floatingPassword'}),
        error_messages={
            'required': "필수 정보입니다.",
        }
    )
    new_password1 = forms.CharField(
        min_length=4,
        label='',
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password",
                   'class': "form-control",
                   'id': 'floatingPassword'}),
        error_messages={
            'required': "필수 정보입니다.",
        }
    )
    new_password2 = None


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content"]
        widgets = {
            'title': TextInput(attrs={
                'placeholder': '제목을 입력해주세요.',
                'class': 'form-control'
            }),
            'content': Textarea(attrs={
                'placeholder': '내용을 입력해주세요.',
                'class': 'form-control'
            })
        }


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
        widgets = {
            'content': Textarea(attrs={
                'placeholder': '내용을 입력해주세요.',
                'class': 'form-control'
            })
        }
