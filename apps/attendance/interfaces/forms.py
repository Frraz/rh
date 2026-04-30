from django import forms
from ..infrastructure.models import Adjustment, DiscountInstallment

CSS = "w-full px-3 py-2.5 border border-slate-300 rounded-lg text-sm focus:ring-2 focus:ring-primary-500 focus:border-primary-500 outline-none transition bg-white"

MONTH_CHOICES = [
    (1, "Janeiro"), (2, "Fevereiro"), (3, "Março"), (4, "Abril"),
    (5, "Maio"), (6, "Junho"), (7, "Julho"), (8, "Agosto"),
    (9, "Setembro"), (10, "Outubro"), (11, "Novembro"), (12, "Dezembro"),
]


class AdjustmentForm(forms.ModelForm):
    reference_month = forms.ChoiceField(
        choices=MONTH_CHOICES,
        label="Mês de referência",
        widget=forms.Select(attrs={"class": CSS}),
    )

    class Meta:
        model = Adjustment
        fields = [
            "person", "adjustment_type", "event_date",
            "reference_year", "reference_month", "value", "description",
        ]
        widgets = {
            "person": forms.Select(attrs={"class": CSS}),
            "adjustment_type": forms.Select(attrs={"class": CSS}),
            "event_date": forms.DateInput(attrs={"class": CSS, "type": "date"}),
            "reference_year": forms.NumberInput(attrs={"class": CSS, "min": 2020, "max": 2099}),
            "value": forms.NumberInput(attrs={"class": CSS, "step": "0.01"}),
            "description": forms.Textarea(attrs={"class": CSS, "rows": 2}),
        }
        labels = {
            "person": "Colaborador",
            "adjustment_type": "Tipo",
            "event_date": "Data do evento",
            "reference_year": "Ano de referência",
            "value": "Valor (negativo = desconto, positivo = crédito)",
            "description": "Descrição",
        }

    def clean_reference_month(self):
        return int(self.cleaned_data["reference_month"])


class InstallmentForm(forms.Form):
    from apps.employees.infrastructure.models import Person as PersonModel

    person = forms.ModelChoiceField(
        queryset=PersonModel.objects.filter(status="active").order_by("name"),
        label="Colaborador",
        widget=forms.Select(attrs={"class": CSS}),
    )
    installment_type = forms.ChoiceField(
        choices=DiscountInstallment.InstallmentType.choices,
        label="Tipo",
        widget=forms.Select(attrs={"class": CSS}),
    )
    description = forms.CharField(
        label="Descrição",
        max_length=200,
        widget=forms.TextInput(attrs={"class": CSS, "placeholder": "Ex: Adiantamento para reforma"}),
    )
    total_value = forms.DecimalField(
        label="Valor total (R$)",
        min_value=0.01,
        widget=forms.NumberInput(attrs={"class": CSS, "step": "0.01", "id": "id_total_value"}),
    )
    num_installments = forms.IntegerField(
        label="Número de parcelas",
        min_value=1,
        max_value=60,
        initial=1,
        widget=forms.NumberInput(attrs={"class": CSS, "min": 1, "max": 60, "id": "id_num_installments"}),
    )
    first_reference_month = forms.ChoiceField(
        choices=MONTH_CHOICES,
        label="Mês inicial do desconto",
        widget=forms.Select(attrs={"class": CSS}),
    )
    first_reference_year = forms.IntegerField(
        label="Ano inicial",
        min_value=2020,
        max_value=2099,
        widget=forms.NumberInput(attrs={"class": CSS}),
    )

    def clean_first_reference_month(self):
        return int(self.cleaned_data["first_reference_month"])
