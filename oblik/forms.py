from django import forms
from .models import ServiceMember
from datetime import date

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class ServiceMemberForm(forms.ModelForm):
    class Meta:
        model = ServiceMember
        exclude = ("user",)
        fields = "__all__"
        widgets = {
            "birth_date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control",
                }
            )
        }

    def clean_birth_date(self):
        birth_date = self.cleaned_data.get("birth_date")

        if birth_date and birth_date > date.today():
            raise forms.ValidationError(
                "Дата народження не може бути в майбутньому"
            )

        return birth_date


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")