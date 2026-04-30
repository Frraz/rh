from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import TemplateView

from .forms import LoginForm, UserProfileForm


class LoginView(View):
    template_name = "accounts/login.html"

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("dashboard:index")
        form = LoginForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            next_url = request.GET.get("next", "/")
            return redirect(next_url)
        return render(request, self.template_name, {"form": form})


class LogoutView(View):
    def post(self, request):
        logout(request)
        return redirect("accounts:login")


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/profile.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["form"] = UserProfileForm(instance=self.request.user)
        ctx["password_form"] = PasswordChangeForm(self.request.user)
        return ctx

    def post(self, request, *args, **kwargs):
        action = request.POST.get("action")

        if action == "update_profile":
            form = UserProfileForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, "Perfil atualizado com sucesso.")
            else:
                messages.error(request, "Erro ao atualizar perfil.")

        elif action == "change_password":
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)
                messages.success(request, "Senha alterada com sucesso.")
            else:
                messages.error(request, "Erro ao alterar senha.")

        return redirect("accounts:profile")


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/index.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        from django.utils import timezone

        from apps.advances.infrastructure.models import Advance
        from apps.employees.infrastructure.models import Person

        hoje = timezone.localdate()
        ctx["hoje"] = hoje.strftime("%d/%m/%Y")
        ctx["total_employees"] = Person.objects.filter(
            person_type="employee", status="active"
        ).count()
        ctx["total_daily"] = Person.objects.filter(
            person_type="daily", status="active"
        ).count()
        ctx["pending_advances"] = Advance.objects.filter(status="pending").count()
        ctx["recent_persons"] = Person.objects.select_related(
            "job_role", "farm"
        ).order_by("-created_at")[:5]
        return ctx
