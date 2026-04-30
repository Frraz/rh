from django import forms
from ..infrastructure.models import Advance

CSS = "w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:ring-2 focus:ring-primary-500 focus:border-primary-500 outline-none transition"


class AdvanceForm(forms.ModelForm):
    class Meta:
        model = Advance
        fields = ["person", "requested_value", "reason"]
        widgets = {
            "person": forms.Select(attrs={"class": CSS}),
            "requested_value": forms.NumberInput(attrs={"class": CSS, "step": "0.01"}),
            "reason": forms.Textarea(attrs={"class": CSS, "rows": 3}),
        }
        labels = {
            "person": "Colaborador",
            "requested_value": "Valor solicitado (R$)",
            "reason": "Motivo da solicitação",
        }


class ApprovalForm(forms.Form):
    approved_value = forms.DecimalField(
        label="Valor aprovado (R$)",
        min_value=0.01,
        widget=forms.NumberInput(attrs={"class": CSS, "step": "0.01"}),
    )
    discount_year = forms.IntegerField(
        label="Ano do desconto",
        widget=forms.NumberInput(attrs={"class": CSS}),
    )
    discount_month = forms.IntegerField(
        label="Mês do desconto",
        min_value=1,
        max_value=12,
        widget=forms.NumberInput(attrs={"class": CSS}),
    )