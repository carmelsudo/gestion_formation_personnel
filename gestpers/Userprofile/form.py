# forms.py
from django import forms
from .models import User
from Service.models import Service

class inscriptionForm(forms.ModelForm):
    password_confirmation = forms.CharField(
        widget=forms.PasswordInput(),
        required=True
    )
    services = forms.ModelChoiceField(
        queryset=Service.objects.all(),
        required=True,
        empty_label="Select a service", # Optional: adds a default "--------- " option
        widget=forms.Select(attrs={}) # Optional: for styling
    )

    class Meta:
        model = User
        fields = ['username' , 'email' , 'password' ,'password_confirmation', 'services']

class ConexionForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ["email", "password"]