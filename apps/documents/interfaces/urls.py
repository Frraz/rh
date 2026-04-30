from django.urls import path
from . import views

app_name = "documents"

urlpatterns = [
    path("", views.DocumentListView.as_view(), name="list"),
    path("novo/", views.DocumentCreateView.as_view(), name="create"),
    path("<int:pk>/excluir/", views.DocumentDeleteView.as_view(), name="delete"),
]