from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile


# Create your forms here
class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "password1", "password2")


class ProfileCompletionForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("email", "blood_type", "caza")
