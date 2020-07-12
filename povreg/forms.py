from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


group_choices = [
    ('Officers', 'Officers'),
    ('Drivers', 'Drivers'),
]


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text="Required. Inform a valid email address.")
    type = forms.CharField(label="Account Type", widget=forms.RadioSelect(choices=group_choices))
    # print(type.clean())

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', ]

