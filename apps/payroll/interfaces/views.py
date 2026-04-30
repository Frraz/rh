from datetime import date
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.views import View

from apps.attendance.infrastructure.models import Adjustment
from apps.employees.infrastructure.models import Entity, Person


class PayrollDashboardView(LoginRequiredMixin, View):
    template_name = "payroll/dashboard.html"

    def get(self, request):
        today = timezone.localdate()
        year = int(request.GET.get("year", today.year))
        month = int(request.GET.get("month", today.month))
        entity_id = request.GET.get("entity", "")

        entities = Entity.objects.all()
        selected_entity = None

        if entity_id:
            try:
                selected_entity = Entity.objects.get(pk=entity_id)
            except Entity.DoesNotExist:
                pass

        persons_qs = Person.objects.select_related("entity", "farm", "job_role").filter(
            status="active"
        )
        if selected_entity:
            persons_qs = persons_qs.filter(entity=selected_entity)

        adjustments_qs = Adjustment.objects.filter(
            reference_year=year,
            reference_month=month,
            is_deleted=False,
        ).select_related("person")

        adjustments_by_person = {}
        for adj in adjustments_qs:
            adjustments_by_person.setdefault(adj.person_id, []).append(adj)

        folha = []
        total_bruto = Decimal("0")
        total_descontos = Decimal("0")
        total_liquido = Decimal("0")

        for person in persons_qs.order_by("entity__name", "name"):
            adjs = adjustments_by_person.get(person.pk, [])
            descontos = sum(a.value for a in adjs if a.value < 0)
            creditos = sum(a.value for a in adjs if a.value > 0)

            if person.is_employee:
                salario_base = person.salary or Decimal("0")
            else:
                salario_base = person.daily_rate or Decimal("0")

            bruto = salario_base + creditos
            liquido = bruto + descontos

            folha.append(
                {
                    "person": person,
                    "salario_base": salario_base,
                    "creditos": creditos,
                    "descontos": descontos,
                    "bruto": bruto,
                    "liquido": liquido,
                    "adjustments": adjs,
                }
            )

            total_bruto += bruto
            total_descontos += descontos
            total_liquido += liquido

        return render(
            request,
            self.template_name,
            {
                "folha": folha,
                "entities": entities,
                "selected_entity": selected_entity,
                "current_year": year,
                "current_month": month,
                "total_bruto": total_bruto,
                "total_descontos": total_descontos,
                "total_liquido": total_liquido,
                "total_pessoas": len(folha),
            },
        )


class PayslipSelectorView(LoginRequiredMixin, View):
    """Tela de seleção de mês/ano/dias antes de gerar o holerite."""

    MESES = {
        1: "Janeiro",
        2: "Fevereiro",
        3: "Março",
        4: "Abril",
        5: "Maio",
        6: "Junho",
        7: "Julho",
        8: "Agosto",
        9: "Setembro",
        10: "Outubro",
        11: "Novembro",
        12: "Dezembro",
    }

    def get(self, request, pk):
        person = get_object_or_404(
            Person.objects.select_related("entity", "farm", "job_role"), pk=pk
        )
        today = timezone.localdate()
        return render(
            request,
            "payroll/payslip_selector.html",
            {
                "person": person,
                "current_year": today.year,
                "current_month": today.month,
                "meses": self.MESES,
            },
        )

    def post(self, request, pk):
        person = get_object_or_404(Person, pk=pk)
        year = request.POST.get("year", "")
        month = request.POST.get("month", "")
        dias = request.POST.get("dias", "0")

        url = f"/folha/holerite/{pk}/?year={year}&month={month}&dias={dias}"
        from django.shortcuts import redirect

        return redirect(url)


class PayslipView(LoginRequiredMixin, View):
    MESES = {
        1: "Janeiro",
        2: "Fevereiro",
        3: "Março",
        4: "Abril",
        5: "Maio",
        6: "Junho",
        7: "Julho",
        8: "Agosto",
        9: "Setembro",
        10: "Outubro",
        11: "Novembro",
        12: "Dezembro",
    }

    def get(self, request, pk):
        person = get_object_or_404(
            Person.objects.select_related("entity", "farm", "job_role"), pk=pk
        )
        today = timezone.localdate()
        year = int(request.GET.get("year", today.year))
        month = int(request.GET.get("month", today.month))
        dias_trabalhados = int(request.GET.get("dias", 0))

        adjustments = (
            Adjustment.objects.filter(
                person=person,
                reference_year=year,
                reference_month=month,
                is_deleted=False,
            )
            .select_related("installment")
            .order_by("adjustment_type")
        )

        descontos = [a for a in adjustments if a.value < 0]
        creditos = [a for a in adjustments if a.value > 0]

        if person.is_employee:
            salario_base = person.salary or Decimal("0")
        else:
            salario_base = (person.daily_rate or Decimal("0")) * dias_trabalhados

        total_creditos = sum(a.value for a in creditos)
        total_descontos = sum(a.value for a in descontos)
        total_proventos = salario_base + total_creditos
        liquido = total_proventos + total_descontos

        return render(
            request,
            "payroll/payslip.html",
            {
                "person": person,
                "year": year,
                "month": month,
                "month_name": self.MESES.get(month, ""),
                "salario_base": salario_base,
                "dias_trabalhados": dias_trabalhados,
                "descontos": descontos,
                "creditos": creditos,
                "total_proventos": total_proventos,
                "total_descontos": abs(total_descontos),
                "liquido": liquido,
            },
        )


class TerminationFormView(LoginRequiredMixin, View):
    template_name = "payroll/termination_form.html"

    def get(self, request):
        today = timezone.localdate()
        persons = Person.objects.filter(status="active").order_by("name")
        return render(
            request,
            self.template_name,
            {
                "persons": persons,
                "today": today.isoformat(),
            },
        )

    def post(self, request):
        from apps.payroll.application.use_cases.calculate_termination import (
            CalculateTerminationUseCase,
            TerminationInputDTO,
        )

        persons = Person.objects.filter(status="active").order_by("name")
        today = timezone.localdate()

        try:
            person_id = int(request.POST.get("person_id", 0))
            person = get_object_or_404(
                Person.objects.select_related("entity", "farm", "job_role"),
                pk=person_id,
            )

            termination_date_str = request.POST.get("termination_date", "")
            termination_date = date.fromisoformat(termination_date_str)

            dto = TerminationInputDTO(
                person_id=person_id,
                termination_type=request.POST.get("termination_type", "without_cause"),
                termination_date=termination_date,
                notice_type=request.POST.get("notice_type", "worked"),
                vacation_days_due=int(request.POST.get("vacation_days_due", 0)),
                vacation_months_prop=int(request.POST.get("vacation_months_prop", 0)),
                fgts_balance=Decimal(request.POST.get("fgts_balance", "0") or "0"),
            )

            result = CalculateTerminationUseCase().execute(dto)
            return render(
                request,
                "payroll/termination_result.html",
                {
                    "result": result,
                    "person": person,
                    "calculated_at": today,
                },
            )

        except (ValueError, Exception) as e:
            messages.error(request, f"Erro no cálculo: {e}")
            return render(
                request,
                self.template_name,
                {
                    "persons": persons,
                    "today": today.isoformat(),
                },
            )


class RubricaReportView(LoginRequiredMixin, View):
    template_name = "payroll/rubrica_report.html"

    MESES = {
        1: "Janeiro",
        2: "Fevereiro",
        3: "Março",
        4: "Abril",
        5: "Maio",
        6: "Junho",
        7: "Julho",
        8: "Agosto",
        9: "Setembro",
        10: "Outubro",
        11: "Novembro",
        12: "Dezembro",
    }

    def get(self, request):
        today = timezone.localdate()
        year = int(request.GET.get("year", today.year))
        month = int(request.GET.get("month", today.month))
        entity_id = request.GET.get("entity", "")

        entities = Entity.objects.all()
        selected_entity = None
        if entity_id:
            try:
                selected_entity = Entity.objects.get(pk=entity_id)
            except Entity.DoesNotExist:
                pass

        qs = Adjustment.objects.filter(
            reference_year=year,
            reference_month=month,
            is_deleted=False,
        ).select_related("person", "person__entity")

        if selected_entity:
            qs = qs.filter(person__entity=selected_entity)

        # Agrupar por tipo
        from collections import defaultdict

        rubricas = defaultdict(
            lambda: {"label": "", "items": [], "total": Decimal("0")}
        )

        for adj in qs:
            tipo = adj.adjustment_type
            rubricas[tipo]["label"] = adj.get_adjustment_type_display()
            rubricas[tipo]["items"].append(adj)
            rubricas[tipo]["total"] += adj.value

        # Ordenar: descontos primeiro, créditos depois
        rubricas_list = sorted(
            rubricas.values(), key=lambda r: (r["total"] >= 0, r["label"])
        )

        total_geral = sum(r["total"] for r in rubricas_list)
        total_descontos = sum(r["total"] for r in rubricas_list if r["total"] < 0)
        total_creditos = sum(r["total"] for r in rubricas_list if r["total"] > 0)

        # Contagem de pessoas por tipo
        pessoas_ids = set()
        for adj in qs:
            pessoas_ids.add(adj.person_id)

        return render(
            request,
            self.template_name,
            {
                "rubricas": rubricas_list,
                "entities": entities,
                "selected_entity": selected_entity,
                "current_year": year,
                "current_month": month,
                "month_name": self.MESES.get(month, ""),
                "total_geral": total_geral,
                "total_descontos": total_descontos,
                "total_creditos": total_creditos,
                "total_pessoas": len(pessoas_ids),
            },
        )
