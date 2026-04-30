from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),

    # Autenticação e dashboard
    path("", include("apps.accounts.interfaces.urls")),

    # Módulos
    path("funcionarios/", include("apps.employees.interfaces.urls")),
    path("documentos/", include("apps.documents.interfaces.urls")),
    path("frequencia/", include("apps.attendance.interfaces.urls")),
    path("adiantamentos/", include("apps.advances.interfaces.urls")),
    path("folha/", include("apps.payroll.interfaces.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    try:
        import debug_toolbar
        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
    except ImportError:
        pass