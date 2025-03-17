from django.conf import settings
from django import forms
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox
from utils.validators import is_validate_birth_date, is_validate_password
from accounts.models import CustomUser


class UserForm(forms.ModelForm):
    username = forms.CharField(
        max_length=20,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter Username."}
        ),
        required=True,
    )
    email = forms.EmailField(
        max_length=120,
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Enter Email."}
        ),
    )
    first_name = forms.CharField(
        max_length=20,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter First Name."}
        ),
        required=False,
    )
    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter Last Name."}
        ),
        required=False,
    )
    avatar = forms.FileField(
        required=False,
        widget=forms.FileInput(
            attrs={"class": "form-control", "placeholder": "Choose Your Picture."}
        ),
    )
    birth_date = forms.DateField(
        required=True,
        widget=forms.DateInput(
            attrs={"class": "form-control", "placeholder": "Enter Birth Date"}
        ),
    )
    password = forms.CharField(
        max_length=128,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Enter Password."}
        ),
        required=True,
    )
    password2 = forms.CharField(
        max_length=128,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Confirm Password"}
        ),
        required=True,
    )
    recaptcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)
    last_login_ip = forms.GenericIPAddressField(
        widget=forms.HiddenInput(), required=False
    )

    class Meta:
        model = CustomUser
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "avatar",
            "birth_date",
            "password",
            "last_login_ip",
            "recaptcha",
        )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password", "")
        password2 = cleaned_data.get("password2", "")
        if not password or not password2:
            raise forms.ValidationError("Please enter your password.")

        if password != password2:
            raise forms.ValidationError("your password did not match.")

        validated_password = is_validate_password(password)
        if isinstance(validated_password, list):
            raise forms.ValidationError(validated_password)

        return cleaned_data

    def clean_birth_date(self):
        birth_date = self.cleaned_data.get("birth_date", "")

        if not birth_date:
            raise forms.ValidationError("Please enter you birth date.")

        if is_validate_birth_date(birth_date):
            raise forms.ValidationError("your age must be at least 18+.")

        return birth_date

    def save(self, commit=...):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(
        max_length=20,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter Username."}
        ),
        required=True,
    )
    email = forms.CharField(
        max_length=120,
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Enter Email."}
        ),
        required=True,
    )
    first_name = forms.CharField(
        max_length=20,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter First Name."}
        ),
        required=False,
    )
    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter Last Name."}
        ),
        required=False,
    )
    avatar = forms.FileField(
        widget=forms.FileInput(
            attrs={"class": "form-control", "placeholder": "Choose Your Picture."}
        ),
        required=False,
    )
    birth_date = forms.DateField(
        widget=forms.DateInput(
            attrs={"class": "form-control", "placeholder": "Enter Birth Date"}
        ),
        required=True,
    )

    class Meta:
        model = CustomUser
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "avatar",
            "birth_date",
        )

    def clean_birth_date(self):
        birth_date = self.cleaned_data.get("birth_date", "")

        if not birth_date:
            raise forms.ValidationError("Please enter you birth date.")

        if is_validate_birth_date(birth_date):
            raise forms.ValidationError("your age must be at leat 18+.")

        return birth_date


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=20,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Username"}
        ),
        label="username",
        required=True,
    )
    password = forms.CharField(
        max_length=20,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Password"}
        ),
        label="password",
        required=True,
    )
    remember_me = forms.BooleanField(required=True)

    def clean_password(self):
        password = self.cleaned_data.get("password")

        if type(is_validate_password(password)) is list:
            raise forms.ValidationError(is_validate_password(password))

        return password


class PasswordForgotForm(forms.Form):
    email = forms.EmailField(max_length=100, label="Email", required=True)

    def clean_email(self):
        email = self.cleaned_data.get("email", "")

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise forms.ValidationError("Your email does not correct.")

        return email


class SetNewPasswordForm(forms.Form):
    password1 = forms.CharField(
        max_length=128,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Enter new password"}
        ),
        label="New Password",
        required=True,
    )
    password2 = forms.CharField(
        max_length=128,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Confirm new password"}
        ),
        label="Confirm Password",
        required=True,
    )

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1", "")
        password2 = cleaned_data.get("password2", "")

        if not password1 or not password2:
            raise forms.ValidationError("You must enter a password.")

        validation_error = is_validate_password(password1)
        if isinstance(validation_error, list):
            raise forms.ValidationError(validation_error)

        if password1 != password2:
            raise forms.ValidationError("your password did not match.")

        return cleaned_data
