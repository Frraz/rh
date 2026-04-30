from django import forms
from ..infrastructure.models import Document, DocumentType

CSS = "w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:ring-2 focus:ring-primary-500 focus:border-primary-500 outline-none transition"


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ["person", "document_type", "file", "number", "issue_date", "expiry_date", "notes"]
        widgets = {
            "person": forms.Select(attrs={"class": CSS}),
            "document_type": forms.Select(attrs={"class": CSS}),
            "number": forms.TextInput(attrs={"class": CSS}),
            "issue_date": forms.DateInput(attrs={"class": CSS, "type": "date"}),
            "expiry_date": forms.DateInput(attrs={"class": CSS, "type": "date"}),
            "notes": forms.Textarea(attrs={"class": CSS, "rows": 2}),
        }