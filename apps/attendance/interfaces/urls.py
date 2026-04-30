from django.urls import path

from . import views

app_name = "attendance"

urlpatterns = [
    # Ajustes avulsos
    path("", views.AdjustmentListView.as_view(), name="list"),
    path("novo/", views.AdjustmentCreateView.as_view(), name="create"),
    path("<int:pk>/excluir/", views.AdjustmentDeleteView.as_view(), name="delete"),
    # Descontos parcelados
    path(
        "parcelamentos/", views.InstallmentListView.as_view(), name="installment_list"
    ),
    path(
        "parcelamentos/novo/",
        views.InstallmentCreateView.as_view(),
        name="installment_create",
    ),
    path(
        "parcelamentos/<int:pk>/",
        views.InstallmentDetailView.as_view(),
        name="installment_detail",
    ),
]
