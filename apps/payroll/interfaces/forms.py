from django import forms
from apps.employees.infrastructure.models import Person
from ..infrastructure.models import Termination

CSS = "w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:ring-2 focus:ring-primary-500 focus:border-primary-500 outline-none transition"


class TerminationForm(forms.Form):
    person = forms.ModelChoiceField(
        queryset=Person.objects.filter(person_type="employee", status="active"),
        label="Funcionário",
        widget=forms.Select(attrs={"class": CSS}),
    )
    termination_type = forms.ChoiceField(
        choices=Termination.TerminationType.choices,
        label="Tipo de demissão",
        widget=forms.Select(attrs={"class": CSS}),
    )
    termination_date = forms.DateField(
        label="Data de demissão",
        widget=forms.DateInput(attrs={"class": CSS, "type": "date"}),
    )
    notice_type = forms.ChoiceField(
        choices=[
            ("worked", "Aviso trabalhado"),
            ("waived", "Aviso indenizado"),
            ("none", "Sem aviso"),
        ],
        label="Aviso prévio",
        widget=forms.Select(attrs={"class": CSS}),
    )
    vacation_days_due = forms.IntegerField(
        label="Dias de férias vencidas",
        min_value=0,
        max_value=30,
        initial=0,
        widget=forms.NumberInput(attrs={"class": CSS}),
    )
    vacation_months_prop = forms.IntegerField(
        label="Meses no período aquisitivo atual",
        min_value=0,
        max_value=12,
        initial=0,
        widget=forms.NumberInput(attrs={"class": CSS}),
    )
    fgts_balance = forms.DecimalField(
        label="Saldo do FGTS (R$)",
        min_value=0,
        initial=0,
        widget=forms.NumberInput(attrs={"class": CSS, "step": "0.01"}),
    )