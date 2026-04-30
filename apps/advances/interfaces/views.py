from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView, View
from django.utils import timezone
from apps.accounts.infrastructure.permissions import HRRequiredMixin
from ..infrastructure.models import Advance
from ..application.use_cases.approve_advance import ApproveAdvanceUseCase
from .forms import AdvanceForm, ApprovalForm
from core.domain.exceptions import DomainException


class AdvanceListView(HRRequiredMixin, ListView):
    model = Advance
    template_name = "advances/list.html"
    context_object_name = "advances"
    paginate_by = 20

    def get_queryset(self):
        qs = Advance.objects.select_related("person", "requested_by").order_by("-request_date")
        status = self.request.GET.get("status", "")
        if status:
            qs = qs.filter(status=status)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["statuses"] = Advance.Status.choices
        ctx["pending_count"] = Advance.objects.filter(status="pending").count()
        return ctx


class AdvanceDetailView(HRRequiredMixin, DetailView):
    model = Advance
    template_name = "advances/detail.html"
    context_object_name = "advance"


class AdvanceCreateView(HRRequiredMixin, View):
    template_name = "advances/form.html"

    def get(self, request):
        return render(request, self.template_name, {"form": AdvanceForm()})

    def post(self, request):
        form = AdvanceForm(request.POST)
        if form.is_valid():
            advance = form.save(commit=False)
            advance.requested_by = request.user
            advance.request_date = timezone.now().date()
            advance.save()
            messages.success(request, "Adiantamento solicitado com sucesso.")
            return redirect("advances:list")
        return render(request, self.template_name, {"form": form})


class AdvanceApproveView(HRRequiredMixin, View):
    def post(self, request, pk):
        advance = get_object_or_404(Advance, pk=pk)
        form = ApprovalForm(request.POST)
        if form.is_valid():
            try:
                use_case = ApproveAdvanceUseCase()
                use_case.execute(
                    advance_id=pk,
                    approved_value=form.cleaned_data["approved_value"],
                    discount_year=form.cleaned_data["discount_year"],
                    discount_month=form.cleaned_data["discount_month"],
                    reviewed_by=request.user,
                )
                messages.success(request, "Adiantamento aprovado e desconto gerado.")
            except DomainException as e:
                messages.error(request, str(e.message))
        return redirect("advances:detail", pk=pk)


class AdvanceRejectView(HRRequiredMixin, View):
    def post(self, request, pk):
        advance = get_object_or_404(Advance, pk=pk)
        reason = request.POST.get("rejection_reason", "").strip()
        if advance.status == Advance.Status.PENDING:
            advance.status = Advance.Status.REJECTED
            advance.rejection_reason = reason
            advance.reviewed_by = request.user
            advance.reviewed_at = timezone.now()
            advance.save()
            messages.success(request, "Adiantamento rejeitado.")
        return redirect("advances:detail", pk=pk)