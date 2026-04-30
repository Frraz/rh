from django.urls import path

from . import views

app_name = "employees"

urlpatterns = [
    path("", views.PersonListView.as_view(), name="list"),
    path("novo/", views.PersonCreateView.as_view(), name="create"),
    path("<int:pk>/", views.PersonDetailView.as_view(), name="detail"),
    path("<int:pk>/editar/", views.PersonUpdateView.as_view(), name="update"),
    path(
        "<int:pk>/desativar/", views.PersonDeactivateView.as_view(), name="deactivate"
    ),
    # HTMX — filtros dinâmicos
    path("htmx/fazendas/", views.HtmxFarmsView.as_view(), name="htmx_farms"),
    path("htmx/funcoes/", views.HtmxJobRolesView.as_view(), name="htmx_jobroles"),
    # Entidades
    path("entidades/", views.EntityListView.as_view(), name="entity_list"),
    path("entidades/nova/", views.EntityCreateView.as_view(), name="entity_create"),
    path(
        "entidades/<int:pk>/editar/",
        views.EntityUpdateView.as_view(),
        name="entity_update",
    ),
    # Fazendas
    path("fazendas/", views.FarmListView.as_view(), name="farm_list"),
    path("fazendas/nova/", views.FarmCreateView.as_view(), name="farm_create"),
    path(
        "fazendas/<int:pk>/editar/", views.FarmUpdateView.as_view(), name="farm_update"
    ),
    # Funções
    path("funcoes/", views.JobRoleListView.as_view(), name="jobrole_list"),
    path("funcoes/nova/", views.JobRoleCreateView.as_view(), name="jobrole_create"),
    path(
        "funcoes/<int:pk>/editar/",
        views.JobRoleUpdateView.as_view(),
        name="jobrole_update",
    ),
]
