from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm
from django.contrib.auth.forms import PasswordResetForm as BasePasswordResetForm
from django.contrib.auth.forms import SetPasswordForm as BaseSetPasswordForm
from django import forms

from .models import MyUser


class UserCreationForm(BaseUserCreationForm):

    class Meta:
        model = MyUser
        fields = ('email', 'dob')


class PasswordResetRequestForm(BasePasswordResetForm):
    email = forms.EmailField(
        label='Email address',
        max_length=254,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'email address',
                'type': 'text',
                'id': 'email_address'
            }
        ))


class PasswordResetForm(BaseSetPasswordForm):
    new_password1 = forms.CharField(
        label='Password',
        help_text="""<ul class='errorlist text-muted'>
            <li>Your password can 't be too similar to your other personal information.</li>
            <li>Your password must contain at least 8 characters.</li>
            <li>Your password can 't be a commonly used password.</li>
            <li>Your password can 't be entirely numeric.<li>
        </ul>""",
        max_length=100,
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'password',
                'type': 'password',
                'id': 'user_password',
            }))

    new_password2 = forms.CharField(
        label='Confirm password',
        help_text=False,
        max_length=100,
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'confirm password',
                'type': 'password',
                'id': 'user_password',
            }))
