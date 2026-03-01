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

        labels = {
            'name': "Ім'я",
            'middle_name': 'По батькові',
            'surname': 'Прізвище',
            'call_sign': 'Позивний',
            'birth_date': 'Дата народження',
            'rank': 'Звання',
            'position': 'Посада',
            'unit': 'Підрозділ',
            'status': 'Статус',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        placeholders = {
            'name': "Введіть ім'я",
            'middle_name': 'Введіть По батькові',
            'surname': 'Введіть прізвище',
            'call_sign': 'Введіть позивний',
            'birth_date': 'Дата народження',
        }

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

            if field_name in placeholders:
                field.widget.attrs['placeholder'] = placeholders[field_name]

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