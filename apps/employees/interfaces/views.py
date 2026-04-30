from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import DetailView, ListView

from apps.accounts.infrastructure.permissions import HRRequiredMixin
from core.domain.exceptions import DomainException

from ..application.dtos import CreatePersonDTO, UpdatePersonDTO
from ..application.use_cases.create_employee import CreatePersonUseCase
from ..application.use_cases.deactivate_employee import DeactivatePersonUseCase
from ..application.use_cases.update_employee import UpdatePersonUseCase
from ..infrastructure.models import Entity, Farm, JobRole, Person
from .forms import EntityForm, FarmForm, JobRoleForm, PersonForm


class PersonListView(HRRequiredMixin, ListView):
    model = Person
    template_name = "employees/list.html"
    context_object_name = "persons"
    paginate_by = 20

    def get_queryset(self):
        qs = Person.objects.select_related("entity", "farm", "job_role").order_by(
            "name"
        )
        search = self.request.GET.get("q", "").strip()
        entity_id = self.request.GET.get("entity", "")
        person_type = self.request.GET.get("type", "")
        status = self.request.GET.get("status", "active")

        if search:
            qs = qs.filter(name__icontains=search) | qs.filter(cpf__icontains=search)
        if entity_id:
            qs = qs.filter(entity_id=entity_id)
        if person_type:
            qs = qs.filter(person_type=person_type)
        if status:
            qs = qs.filter(status=status)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["entities"] = Entity.objects.all()
        ctx["person_types"] = Person.PersonType.choices
        ctx["total"] = self.get_queryset().count()
        return ctx


class PersonDetailView(HRRequiredMixin, DetailView):
    model = Person
    template_name = "employees/detail.html"
    context_object_name = "person"

    def get_queryset(self):
        return Person.objects.select_related("entity", "farm", "job_role")


class PersonCreateView(HRRequiredMixin, View):
    template_name = "employees/form.html"

    def get(self, request):
        return render(
            request, self.template_name, {"form": PersonForm(), "action": "create"}
        )

    def post(self, request):
        form = PersonForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                dto = CreatePersonDTO(**form.cleaned_data_as_dto())
                person = CreatePersonUseCase().execute(dto)
                messages.success(
                    request, f"Colaborador {person.name} cadastrado com sucesso."
                )
                return redirect("employees:detail", pk=person.pk)
            except DomainException as e:
                messages.error(request, str(e.message))
        return render(request, self.template_name, {"form": form, "action": "create"})


class PersonUpdateView(HRRequiredMixin, View):
    template_name = "employees/form.html"

    def get(self, request, pk):
        person = get_object_or_404(Person, pk=pk)
        return render(
            request,
            self.template_name,
            {"form": PersonForm(instance=person), "person": person, "action": "edit"},
        )

    def post(self, request, pk):
        person = get_object_or_404(Person, pk=pk)
        form = PersonForm(request.POST, request.FILES, instance=person)
        if form.is_valid():
            try:
                dto = UpdatePersonDTO(person_id=person.pk, **form.cleaned_data_as_dto())
                updated = UpdatePersonUseCase().execute(dto)
                messages.success(
                    request, f"Colaborador {updated.name} atualizado com sucesso."
                )
                return redirect("employees:detail", pk=updated.pk)
            except DomainException as e:
                messages.error(request, str(e.message))
        return render(
            request,
            self.template_name,
            {"form": form, "person": person, "action": "edit"},
        )


class PersonDeactivateView(HRRequiredMixin, View):
    def post(self, request, pk):
        try:
            person = DeactivatePersonUseCase().execute(pk)
            messages.success(request, f"Colaborador {person.name} desativado.")
        except DomainException as e:
            messages.error(request, str(e.message))
        return redirect("employees:list")


# --- Entidade ---


class EntityListView(HRRequiredMixin, ListView):
    model = Entity
    template_name = "employees/entity_list.html"
    context_object_name = "entities"

    def get_queryset(self):
        return Entity.objects.all()


class EntityCreateView(HRRequiredMixin, View):
    template_name = "employees/entity_form.html"

    def get(self, request):
        return render(
            request, self.template_name, {"form": EntityForm(), "action": "create"}
        )

    def post(self, request):
        form = EntityForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Entidade cadastrada com sucesso.")
            return redirect("employees:entity_list")
        return render(request, self.template_name, {"form": form, "action": "create"})


class EntityUpdateView(HRRequiredMixin, View):
    template_name = "employees/entity_form.html"

    def get(self, request, pk):
        entity = get_object_or_404(Entity, pk=pk)
        return render(
            request,
            self.template_name,
            {"form": EntityForm(instance=entity), "entity": entity, "action": "edit"},
        )

    def post(self, request, pk):
        entity = get_object_or_404(Entity, pk=pk)
        form = EntityForm(request.POST, instance=entity)
        if form.is_valid():
            form.save()
            messages.success(request, "Entidade atualizada com sucesso.")
            return redirect("employees:entity_list")
        return render(
            request,
            self.template_name,
            {"form": form, "entity": entity, "action": "edit"},
        )


# --- Fazenda ---


class FarmListView(HRRequiredMixin, ListView):
    model = Farm
    template_name = "employees/farm_list.html"
    context_object_name = "farms"

    def get_queryset(self):
        return Farm.objects.select_related("entity").order_by("entity__name", "name")


class FarmCreateView(HRRequiredMixin, View):
    template_name = "employees/farm_form.html"

    def get(self, request):
        return render(
            request, self.template_name, {"form": FarmForm(), "action": "create"}
        )

    def post(self, request):
        form = FarmForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Fazenda cadastrada com sucesso.")
            return redirect("employees:farm_list")
        return render(request, self.template_name, {"form": form, "action": "create"})


class FarmUpdateView(HRRequiredMixin, View):
    template_name = "employees/farm_form.html"

    def get(self, request, pk):
        farm = get_object_or_404(Farm, pk=pk)
        return render(
            request,
            self.template_name,
            {"form": FarmForm(instance=farm), "farm": farm, "action": "edit"},
        )

    def post(self, request, pk):
        farm = get_object_or_404(Farm, pk=pk)
        form = FarmForm(request.POST, instance=farm)
        if form.is_valid():
            form.save()
            messages.success(request, "Fazenda atualizada com sucesso.")
            return redirect("employees:farm_list")
        return render(
            request, self.template_name, {"form": form, "farm": farm, "action": "edit"}
        )


# --- Função ---


class JobRoleListView(HRRequiredMixin, ListView):
    model = JobRole
    template_name = "employees/jobrole_list.html"
    context_object_name = "job_roles"

    def get_queryset(self):
        return JobRole.objects.select_related("entity").order_by("entity__name", "name")


class JobRoleCreateView(HRRequiredMixin, View):
    template_name = "employees/jobrole_form.html"

    def get(self, request):
        return render(
            request, self.template_name, {"form": JobRoleForm(), "action": "create"}
        )

    def post(self, request):
        form = JobRoleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Função cadastrada com sucesso.")
            return redirect("employees:jobrole_list")
        return render(request, self.template_name, {"form": form, "action": "create"})


class JobRoleUpdateView(HRRequiredMixin, View):
    template_name = "employees/jobrole_form.html"

    def get(self, request, pk):
        role = get_object_or_404(JobRole, pk=pk)
        return render(
            request,
            self.template_name,
            {"form": JobRoleForm(instance=role), "role": role, "action": "edit"},
        )

    def post(self, request, pk):
        role = get_object_or_404(JobRole, pk=pk)
        form = JobRoleForm(request.POST, instance=role)
        if form.is_valid():
            form.save()
            messages.success(request, "Função atualizada com sucesso.")
            return redirect("employees:jobrole_list")
        return render(
            request, self.template_name, {"form": form, "role": role, "action": "edit"}
        )


# --- HTMX ---


class HtmxFarmsView(View):
    """Retorna options de fazendas filtradas por entidade. Usado pelo formulário de colaborador via HTMX/fetch."""

    def get(self, request):
        entity_id = request.GET.get("entity", "").strip()
        options = '<option value="">Selecione a fazenda</option>'
        if entity_id:
            for farm in Farm.objects.filter(entity_id=entity_id).order_by("name"):
                options += f'<option value="{farm.pk}">{farm.name}</option>'
        return HttpResponse(options)


class HtmxJobRolesView(View):
    """Retorna options de funções filtradas por entidade. Usado pelo formulário de colaborador via HTMX/fetch."""

    def get(self, request):
        entity_id = request.GET.get("entity", "").strip()
        options = '<option value="">Selecione a função</option>'
        if entity_id:
            for role in JobRole.objects.filter(entity_id=entity_id).order_by("name"):
                options += f'<option value="{role.pk}">{role.name}</option>'
        return HttpResponse(options)


class PersonDetailView(HRRequiredMixin, DetailView):
    model = Person
    template_name = "employees/detail.html"
    context_object_name = "person"

    def get_queryset(self):
        return Person.objects.select_related("entity", "farm", "job_role")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        from apps.attendance.infrastructure.models import (
            Adjustment,
            DiscountInstallment,
        )

        person = self.object
        ctx["recent_adjustments"] = Adjustment.objects.filter(
            person=person, is_deleted=False
        ).order_by("-reference_year", "-reference_month")[:10]
        ctx["active_installments"] = DiscountInstallment.objects.filter(
            person=person, is_deleted=False
        ).order_by("-created_at")
        return ctx
