from django import forms
from .models import Customer

# from django.contrib.auth import password_validation
from django.contrib.auth import password_validation
from django.contrib.auth.models import User
from django.contrib.auth.forms import (
    PasswordChangeForm,
    UserCreationForm,
    AuthenticationForm,
    UsernameField,
    PasswordResetForm,
    SetPasswordForm,
)
from django.utils.translation import gettext, gettext_lazy as _


# registration form


class CustomerRegistrationForm(UserCreationForm):
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(
            attrs={
                "class": (
                    "w-full px-4 py-3 border border-gray-300 rounded-lg "
                    "focus:outline-none focus:ring-2 focus:ring-indigo-500 "
                    "focus:border-indigo-500 transition"
                ),
                "placeholder": "Enter your username",
                "autocomplete": "username",
            }
        ),
    )

    email = forms.EmailField(
        label="Email",
        required=True,
        widget=forms.EmailInput(
            attrs={
                "class": (
                    "w-full px-4 py-3 border border-gray-300 rounded-lg "
                    "focus:outline-none focus:ring-2 focus:ring-indigo-500 "
                    "focus:border-indigo-500 transition"
                ),
                "placeholder": "Enter your email address",
                "autocomplete": "email",
            }
        ),
    )

    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "class": (
                    "w-full px-4 py-3 border border-gray-300 rounded-lg "
                    "focus:outline-none focus:ring-2 focus:ring-indigo-500 "
                    "focus:border-indigo-500 transition"
                ),
                "placeholder": "Create a password",
                "autocomplete": "new-password",
            }
        ),
    )

    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(
            attrs={
                "class": (
                    "w-full px-4 py-3 border border-gray-300 rounded-lg "
                    "focus:outline-none focus:ring-2 focus:ring-indigo-500 "
                    "focus:border-indigo-500 transition"
                ),
                "placeholder": "Confirm your password",
                "autocomplete": "new-password",
            }
        ),
    )

    class Meta:
        model = User

        fields = [
            "username",
            "email",
            "password1",
            "password2",
        ]


# login form


class LoginForm(AuthenticationForm):
    username = UsernameField(
        widget=forms.TextInput(
            attrs={
                "autofocus": True,
                "class": (
                    "w-full px-4 py-3 border border-gray-300 rounded-lg "
                    "focus:outline-none focus:ring-2 focus:ring-indigo-500 "
                    "focus:border-indigo-500 transition"
                ),
                "placeholder": "Enter your username",
            }
        )
    )

    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "current-password",
                "class": (
                    "w-full px-4 py-3 border border-gray-300 rounded-lg "
                    "focus:outline-none focus:ring-2 focus:ring-indigo-500 "
                    "focus:border-indigo-500 transition"
                ),
                "placeholder": "Enter your password",
            }
        ),
    )


# password change form


class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label=_("Old Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "current-password",
                "autofocus": True,
                "class": (
                    "w-full px-4 pl-10 py-3 border border-gray-300 rounded-lg "
                    "focus:outline-none focus:ring-2 focus:ring-indigo-500 "
                    "focus:border-indigo-500 transition"
                ),
                "placeholder": "Enter your old password",
            }
        ),
    )
    new_password1 = forms.CharField(
        label=_("New Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
                "class": (
                    "w-full px-4 pl-10 py-3 border border-gray-300 rounded-lg "
                    "focus:outline-none focus:ring-2 focus:ring-indigo-500 "
                    "focus:border-indigo-500 transition"
                ),
                "placeholder": "Enter your new password",
            }
        ),
        # help_text=password_validation.password_validators_help_text_html()
    )
    new_password2 = forms.CharField(
        label=_("Confirm New Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
                "class": (
                    "w-full px-4 pl-10 py-3 border border-gray-300 rounded-lg "
                    "focus:outline-none focus:ring-2 focus:ring-indigo-500 "
                    "focus:border-indigo-500 transition"
                ),
                "placeholder": "Confirm your new password",
            }
        ),
        # help_text=password_validation.password_validators_help_text_html()
    )


# password reset form


class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label=_("Email"),
        required=True,
        widget=forms.EmailInput(
            attrs={
                "class": (
                    "w-full px-4 pl-10 py-3 border border-gray-300 rounded-lg "
                    "focus:outline-none focus:ring-2 focus:ring-indigo-500 "
                    "focus:border-indigo-500 transition"
                ),
                "placeholder": "Enter your email address",
                "autocomplete": "email",
            }
        ),
    )


class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label=_("New Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
                "class": (
                    "w-full px-4 pl-10 py-3 border border-gray-300 rounded-lg "
                    "focus:outline-none focus:ring-2 focus:ring-indigo-500 "
                    "focus:border-indigo-500 transition"
                ),
                "placeholder": "Enter your new password",
            }
        ),
    )

    new_password2 = forms.CharField(
        label=_("Confirm New Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
                "class": (
                    "w-full px-4 pl-10 py-3 border border-gray-300 rounded-lg "
                    "focus:outline-none focus:ring-2 focus:ring-indigo-500 "
                    "focus:border-indigo-500 transition"
                ),
                "placeholder": "Confirm your new password",
            }
        ),
    )
class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ["name", "district", "thana", "zipcode", "phone", "village"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": (
                        "w-full px-4 py-3 border border-gray-300 rounded-lg "
                        "focus:outline-none focus:ring-2 focus:ring-indigo-500 "
                        "focus:border-indigo-500 transition"
                    ),
                    "placeholder": "Enter your name",
                }
            ),
            "district": forms.Select(
                attrs={
                    "class": (
                        "w-full px-4 py-3 border border-gray-300 rounded-lg "
                        "focus:outline-none focus:ring-2 focus:ring-indigo-500 "
                        "focus:border-indigo-500 transition"
                    )
                }
            ),
            "thana": forms.TextInput(
                attrs={
                    "class": (
                        "w-full px-4 py-3 border border-gray-300 rounded-lg "
                        "focus:outline-none focus:ring-2 focus:ring-indigo-500 "
                        "focus:border-indigo-500 transition"
                    ),
                    "placeholder": "Enter your thana",
                }
            ),
            "zipcode": forms.TextInput(
                attrs={
                    "class": (
                        "w-full px-4 py-3 border border-gray-300 rounded-lg "
                        "focus:outline-none focus:ring-2 focus:ring-indigo-500 "
                        "focus:border-indigo-500 transition"
                    ),
                    "placeholder": "Enter your zipcode",
                }
            ),
            "phone": forms.TextInput(
                attrs={
                    "class": (
                        "w-full px-4 py-3 border border-gray-300 rounded-lg "
                        "focus:outline-none focus:ring-2 focus:ring-indigo-500 "
                        "focus:border-indigo-500 transition"
                    ),
                    "placeholder": "Enter your phone number",
                }
            ),
            'village': forms.TextInput(
                attrs={
                    'class': (
                        'w-full px-4 py-3 border border-gray-300 rounded-lg '
                        'focus:outline-none focus:ring-2 focus:ring-indigo-500 '
                        'focus:border-indigo-500 transition'
                    ),
                    'placeholder': 'Enter your village',
                }
            ),
        }