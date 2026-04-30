from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView, View
from apps.accounts.infrastructure.permissions import HRRequiredMixin
from ..infrastructure.models import Document, DocumentType
from .forms import DocumentForm


class DocumentListView(HRRequiredMixin, ListView):
    model = Document
    template_name = "documents/list.html"
    context_object_name = "documents"
    paginate_by = 20

    def get_queryset(self):
        qs = Document.objects.select_related("person", "document_type").order_by("-created_at")

        person_id = self.request.GET.get("person", "")
        status = self.request.GET.get("status", "")
        doc_type = self.request.GET.get("type", "")

        if person_id:
            qs = qs.filter(person_id=person_id)
        if status:
            qs = qs.filter(status=status)
        if doc_type:
            qs = qs.filter(document_type_id=doc_type)

        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["document_types"] = DocumentType.objects.all()
        ctx["statuses"] = Document.Status.choices
        return ctx


class DocumentCreateView(HRRequiredMixin, View):
    template_name = "documents/form.html"

    def get(self, request):
        person_id = request.GET.get("person")
        initial = {"person": person_id} if person_id else {}
        form = DocumentForm(initial=initial)
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save()
            messages.success(request, "Documento cadastrado com sucesso.")
            return redirect("documents:list")
        return render(request, self.template_name, {"form": form})


class DocumentDeleteView(HRRequiredMixin, View):
    def post(self, request, pk):
        document = get_object_or_404(Document, pk=pk)
        document.soft_delete()
        messages.success(request, "Documento removido.")
        return redirect("documents:list")