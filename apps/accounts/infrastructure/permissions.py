from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied


class RoleRequiredMixin(LoginRequiredMixin):
    """
    Controle de acesso por perfil.
    Corrigido: dispatch chama a view apenas uma vez.
    """
    required_roles = []

    def dispatch(self, request, *args, **kwargs):
        # Usuário não autenticado — LoginRequiredMixin redireciona para login
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        # Superusuário tem acesso irrestrito
        if request.user.is_superuser:
            return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)

        # Verificar perfil
        if self.required_roles and request.user.role not in self.required_roles:
            raise PermissionDenied("Você não tem permissão para acessar esta página.")

        # Acesso permitido
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)


class AdminRequiredMixin(RoleRequiredMixin):
    required_roles = ["admin"]


class HRRequiredMixin(RoleRequiredMixin):
    required_roles = ["admin", "hr"]


class ManagerRequiredMixin(RoleRequiredMixin):
    required_roles = ["admin", "hr", "manager"]