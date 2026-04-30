from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, View
from django.utils import timezone

from apps.accounts.infrastructure.permissions import HRRequiredMixin
from core.domain.exceptions import DomainException
from ..infrastructure.models import Adjustment, DiscountInstallment
from ..application.use_cases.create_installment import CreateInstallmentDTO, CreateInstallmentUseCase
from .forms import AdjustmentForm, InstallmentForm


class AdjustmentListView(HRRequiredMixin, ListView):
    template_name = "attendance/list.html"
    context_object_name = "adjustments"
    paginate_by = 25

    def get_queryset(self):
        today = timezone.now()
        year = int(self.request.GET.get("year", today.year))
        month = int(self.request.GET.get("month", today.month))
        adj_type = self.request.GET.get("type", "")
        person_id = self.request.GET.get("person", "")

        qs = Adjustment.objects.select_related(
            "person", "created_by", "installment"
        ).filter(reference_year=year, reference_month=month)

        if adj_type:
            qs = qs.filter(adjustment_type=adj_type)
        if person_id:
            qs = qs.filter(person_id=person_id)

        return qs.order_by("person__name", "adjustment_type")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        today = timezone.now()
        ctx["adjustment_types"] = Adjustment.AdjustmentType.choices
        ctx["current_year"] = int(self.request.GET.get("year", today.year))
        ctx["current_month"] = int(self.request.GET.get("month", today.month))
        qs = self.get_queryset()
        ctx["total_discounts"] = sum(a.value for a in qs if a.value < 0)
        ctx["total_credits"] = sum(a.value for a in qs if a.value > 0)
        return ctx


class AdjustmentCreateView(HRRequiredMixin, View):
    template_name = "attendance/form.html"

    def get(self, request):
        today = timezone.now()
        initial = {
            "reference_year": today.year,
            "reference_month": today.month,
            "event_date": today.date(),
        }
        if request.GET.get("person"):
            initial["person"] = request.GET.get("person")
        return render(request, self.template_name, {"form": AdjustmentForm(initial=initial)})

    def post(self, request):
        form = AdjustmentForm(request.POST)
        if form.is_valid():
            adjustment = form.save(commit=False)
            adjustment.created_by = request.user
            adjustment.origin = Adjustment.Origin.MANUAL
            adjustment.save()
            messages.success(request, "Ajuste registrado com sucesso.")
            return redirect("attendance:list")
        return render(request, self.template_name, {"form": form})


class AdjustmentDeleteView(HRRequiredMixin, View):
    def post(self, request, pk):
        adjustment = get_object_or_404(Adjustment, pk=pk)
        if adjustment.origin != Adjustment.Origin.MANUAL:
            messages.error(
                request,
                "Ajustes gerados automaticamente não podem ser excluídos diretamente. "
                "Cancele o parcelamento correspondente."
            )
            return redirect("attendance:list")
        adjustment.soft_delete()
        messages.success(request, "Ajuste removido.")
        return redirect("attendance:list")


class InstallmentListView(HRRequiredMixin, ListView):
    template_name = "attendance/installment_list.html"
    context_object_name = "installments"
    paginate_by = 20

    def get_queryset(self):
        qs = DiscountInstallment.objects.select_related("person", "created_by")
        person_id = self.request.GET.get("person", "")
        if person_id:
            qs = qs.filter(person_id=person_id)
        return qs.order_by("-created_at")


class InstallmentCreateView(HRRequiredMixin, View):
    template_name = "attendance/installment_form.html"

    def get(self, request):
        today = timezone.now()
        initial = {
            "first_reference_year": today.year,
            "first_reference_month": today.month,
        }
        if request.GET.get("person"):
            initial["person"] = request.GET.get("person")
        return render(request, self.template_name, {"form": InstallmentForm(initial=initial)})

    def post(self, request):
        form = InstallmentForm(request.POST)
        if form.is_valid():
            try:
                dto = CreateInstallmentDTO(
                    person_id=form.cleaned_data["person"].pk,
                    installment_type=form.cleaned_data["installment_type"],
                    description=form.cleaned_data["description"],
                    total_value=form.cleaned_data["total_value"],
                    num_installments=form.cleaned_data["num_installments"],
                    first_reference_year=form.cleaned_data["first_reference_year"],
                    first_reference_month=form.cleaned_data["first_reference_month"],
                    created_by_id=request.user.pk,
                )
                installment = CreateInstallmentUseCase().execute(dto)
                messages.success(
                    request,
                    f"Parcelamento criado: {installment.num_installments} parcelas de "
                    f"R$ {installment.installment_value} geradas com sucesso."
                )
                return redirect("attendance:installment_list")
            except DomainException as e:
                messages.error(request, e.message)
        return render(request, self.template_name, {"form": form})


class InstallmentDetailView(HRRequiredMixin, View):
    template_name = "attendance/installment_detail.html"

    def get(self, request, pk):
        installment = get_object_or_404(
            DiscountInstallment.objects.select_related("person", "created_by"),
            pk=pk
        )
        parcelas = installment.adjustments.filter(is_deleted=False).order_by(
            "reference_year", "reference_month"
        )
        return render(request, self.template_name, {
            "installment": installment,
            "parcelas": parcelas,
        })
