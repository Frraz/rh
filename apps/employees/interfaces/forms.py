from django import forms
from ..infrastructure.models import Person, Entity, Farm, JobRole


CSS_CLASS = "w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:ring-2 focus:ring-primary-500 focus:border-primary-500 outline-none transition"


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = [
            "entity", "farm", "job_role", "person_type",
            "name", "cpf", "rg", "birth_date", "phone",
            "marital_status", "address", "photo",
            "admission_date", "pis", "ctps",
            "salary", "daily_rate",
            "bank", "bank_agency", "bank_account",
            "notes",
        ]
        widgets = {
            "entity": forms.Select(attrs={"class": CSS_CLASS, "x-model": "entityId", "@change": "loadFarms()"}),
            "farm": forms.Select(attrs={"class": CSS_CLASS}),
            "job_role": forms.Select(attrs={"class": CSS_CLASS}),
            "person_type": forms.Select(attrs={"class": CSS_CLASS, "x-model": "personType"}),
            "name": forms.TextInput(attrs={"class": CSS_CLASS}),
            "cpf": forms.TextInput(attrs={"class": CSS_CLASS, "placeholder": "000.000.000-00"}),
            "rg": forms.TextInput(attrs={"class": CSS_CLASS}),
            "birth_date": forms.DateInput(attrs={"class": CSS_CLASS, "type": "date"}),
            "phone": forms.TextInput(attrs={"class": CSS_CLASS}),
            "marital_status": forms.Select(attrs={"class": CSS_CLASS}),
            "address": forms.Textarea(attrs={"class": CSS_CLASS, "rows": 2}),
            "admission_date": forms.DateInput(attrs={"class": CSS_CLASS, "type": "date"}),
            "pis": forms.TextInput(attrs={"class": CSS_CLASS}),
            "ctps": forms.TextInput(attrs={"class": CSS_CLASS}),
            "salary": forms.NumberInput(attrs={"class": CSS_CLASS, "step": "0.01"}),
            "daily_rate": forms.NumberInput(attrs={"class": CSS_CLASS, "step": "0.01"}),
            "bank": forms.TextInput(attrs={"class": CSS_CLASS}),
            "bank_agency": forms.TextInput(attrs={"class": CSS_CLASS}),
            "bank_account": forms.TextInput(attrs={"class": CSS_CLASS}),
            "notes": forms.Textarea(attrs={"class": CSS_CLASS, "rows": 3}),
        }
        labels = {
            "entity": "Entidade", "farm": "Fazenda", "job_role": "Função",
            "person_type": "Tipo de contrato", "name": "Nome completo",
            "cpf": "CPF", "rg": "RG", "birth_date": "Data de nascimento",
            "phone": "Telefone", "marital_status": "Estado civil",
            "address": "Endereço", "admission_date": "Data de admissão",
            "pis": "PIS/PASEP", "ctps": "CTPS",
            "salary": "Salário mensal (CLT)", "daily_rate": "Valor da diária",
            "bank": "Banco", "bank_agency": "Agência", "bank_account": "Conta",
            "notes": "Observações", "photo": "Foto",
        }

    def cleaned_data_as_dto(self) -> dict:
        """Converte cleaned_data para dict compatível com o DTO."""
        data = self.cleaned_data
        return {
            "name": data["name"],
            "cpf": data["cpf"],
            "person_type": data["person_type"],
            "entity_id": data["entity"].pk,
            "farm_id": data["farm"].pk,
            "job_role_id": data["job_role"].pk,
            "admission_date": data["admission_date"],
            "salary": data.get("salary") or 0,
            "daily_rate": data.get("daily_rate") or 0,
            "phone": data.get("phone", ""),
            "birth_date": data.get("birth_date"),
            "rg": data.get("rg", ""),
            "pis": data.get("pis", ""),
            "ctps": data.get("ctps", ""),
            "marital_status": data.get("marital_status", ""),
            "address": data.get("address", ""),
            "bank": data.get("bank", ""),
            "bank_agency": data.get("bank_agency", ""),
            "bank_account": data.get("bank_account", ""),
            "notes": data.get("notes", ""),
        }


class EntityForm(forms.ModelForm):
    class Meta:
        model = Entity
        fields = ["name", "cnpj", "address", "phone", "email"]
        widgets = {
            "name": forms.TextInput(attrs={"class": CSS_CLASS}),
            "cnpj": forms.TextInput(attrs={"class": CSS_CLASS, "placeholder": "00.000.000/0000-00"}),
            "address": forms.Textarea(attrs={"class": CSS_CLASS, "rows": 2}),
            "phone": forms.TextInput(attrs={"class": CSS_CLASS}),
            "email": forms.EmailInput(attrs={"class": CSS_CLASS}),
        }


class FarmForm(forms.ModelForm):
    class Meta:
        model = Farm
        fields = ["entity", "name", "city", "state"]
        widgets = {
            "entity": forms.Select(attrs={"class": CSS_CLASS}),
            "name": forms.TextInput(attrs={"class": CSS_CLASS}),
            "city": forms.TextInput(attrs={"class": CSS_CLASS}),
            "state": forms.TextInput(attrs={"class": CSS_CLASS, "maxlength": 2}),
        }


class JobRoleForm(forms.ModelForm):
    class Meta:
        model = JobRole
        fields = ["entity", "name"]
        widgets = {
            "entity": forms.Select(attrs={"class": CSS_CLASS}),
            "name": forms.TextInput(attrs={"class": CSS_CLASS}),
        }