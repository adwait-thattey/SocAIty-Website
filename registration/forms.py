from django.contrib.auth.models import User
import django.forms as forms
from django.core.exceptions import ValidationError


class RegisterForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']

    def clean(self):
        cleaned_data = super().clean()

        username = cleaned_data.get("username")

        user_qset = User.objects.filter(username=username)

        if len(user_qset) > 0:
            self.add_error("username", "This username already exists. Please choose another")

        email = cleaned_data.get("email")

        email_qset = User.objects.filter(email=username)

        if len(email_qset) > 0:
            self.add_error("email",
                           "A user with this email already exists. Please login with your account or choose different email id")

        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            self.add_error('confirm_password', "Both Passwords do not match!")
