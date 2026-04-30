from django import forms
from django.contrib.auth.forms import AuthenticationForm
from ..infrastructure.models import User


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Usuário",
        widget=forms.TextInput(attrs={
            "class": "w-full px-4 py-2.5 border border-slate-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 outline-none transition",
            "placeholder": "Nome de usuário",
            "autofocus": True,
        }),
    )
    password = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={
            "class": "w-full px-4 py-2.5 border border-slate-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 outline-none transition",
            "placeholder": "Senha",
        }),
    )


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "phone"]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "input-field"}),
            "last_name": forms.TextInput(attrs={"class": "input-field"}),
            "email": forms.EmailInput(attrs={"class": "input-field"}),
            "phone": forms.TextInput(attrs={"class": "input-field"}),
        }
        labels = {
            "first_name": "Nome",
            "last_name": "Sobrenome",
            "email": "E-mail",
            "phone": "Telefone",
        }


class UserForm(forms.ModelForm):
    """Formulário para criação/edição de usuários pelo admin do sistema."""
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "role", "entity", "is_active"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "input-field"}),
            "first_name": forms.TextInput(attrs={"class": "input-field"}),
            "last_name": forms.TextInput(attrs={"class": "input-field"}),
            "email": forms.EmailInput(attrs={"class": "input-field"}),
            "role": forms.Select(attrs={"class": "input-field"}),
            "entity": forms.Select(attrs={"class": "input-field"}),
        }