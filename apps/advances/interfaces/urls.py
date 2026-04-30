from django.urls import path
from . import views

app_name = "advances"

urlpatterns = [
    path("", views.AdvanceListView.as_view(), name="list"),
    path("novo/", views.AdvanceCreateView.as_view(), name="create"),
    path("<int:pk>/", views.AdvanceDetailView.as_view(), name="detail"),
    path("<int:pk>/aprovar/", views.AdvanceApproveView.as_view(), name="approve"),
    path("<int:pk>/rejeitar/", views.AdvanceRejectView.as_view(), name="reject"),
]