"""
Mixins utilitários para views do módulo de contas.
Centraliza lógica de contexto comum.
"""
from django.contrib.auth.mixins import LoginRequiredMixin


class BreadcrumbMixin:
    """
    Adiciona breadcrumb ao contexto para navegação.
    Uso: defina breadcrumbs = [("Label", "url_name"), ...] na view.
    """
    breadcrumbs = []

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["breadcrumbs"] = self.breadcrumbs
        return ctx