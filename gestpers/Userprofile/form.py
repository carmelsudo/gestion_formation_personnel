# forms.py
from django import forms
from .models import User

class inscriptionForm(forms.ModelForm):
    password_confirmation = forms.CharField(
        widget=forms.PasswordInput(),
        required=True
    )

    class Meta:
        model = User
        fields = ['username' , 'email' , 'password' ,'password_confirmation']

class ConexionForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ["email", "password"]