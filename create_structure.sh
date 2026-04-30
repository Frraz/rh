#!/bin/bash
# =============================================================================
# Script de criação da estrutura do projeto RH
# Execute dentro da pasta raiz: bash create_structure.sh
# =============================================================================

set -e

echo "=========================================="
echo "  Criando estrutura do projeto RH"
echo "=========================================="

# --- Arquivos raiz ---
touch .env.example .gitignore docker-compose.yml Dockerfile Makefile manage.py
touch package.json tailwind.config.js

# --- Requirements ---
mkdir -p requirements
touch requirements/base.txt requirements/development.txt requirements/production.txt

# --- Nginx ---
mkdir -p nginx
touch nginx/nginx.conf nginx/Dockerfile

# --- Config (settings do Django) ---
mkdir -p config/settings
touch config/__init__.py
touch config/settings/__init__.py
touch config/settings/base.py
touch config/settings/development.py
touch config/settings/production.py
touch config/urls.py config/wsgi.py config/asgi.py config/celery.py

# --- Core (camada base: Domain, Application, Infrastructure) ---
mkdir -p core/domain/entities
mkdir -p core/domain/value_objects
mkdir -p core/domain/repositories
mkdir -p core/application/use_cases
mkdir -p core/infrastructure/models
mkdir -p core/shared/utils

touch core/__init__.py
touch core/domain/__init__.py
touch core/domain/entities/__init__.py core/domain/entities/base.py
touch core/domain/value_objects/__init__.py core/domain/value_objects/base.py
touch core/domain/repositories/__init__.py core/domain/repositories/base.py
touch core/domain/exceptions.py
touch core/application/__init__.py
touch core/application/use_cases/__init__.py core/application/use_cases/base.py
touch core/infrastructure/__init__.py
touch core/infrastructure/models/__init__.py core/infrastructure/models/base.py
touch core/shared/__init__.py
touch core/shared/utils/__init__.py
touch core/shared/utils/date_utils.py
touch core/shared/utils/currency_utils.py
touch core/shared/utils/cpf_utils.py

# --- Apps ---
mkdir -p apps
touch apps/__init__.py

# Função auxiliar para criar estrutura padrão de cada app
create_app_structure() {
    local APP=$1
    mkdir -p apps/$APP/domain
    mkdir -p apps/$APP/application/use_cases
    mkdir -p apps/$APP/infrastructure
    mkdir -p apps/$APP/interfaces/templates/$APP

    touch apps/$APP/__init__.py
    touch apps/$APP/apps.py
    touch apps/$APP/domain/__init__.py
    touch apps/$APP/domain/entities.py
    touch apps/$APP/domain/repositories.py
    touch apps/$APP/domain/exceptions.py
    touch apps/$APP/application/__init__.py
    touch apps/$APP/application/dtos.py
    touch apps/$APP/application/use_cases/__init__.py
    touch apps/$APP/infrastructure/__init__.py
    touch apps/$APP/infrastructure/models.py
    touch apps/$APP/infrastructure/repositories.py
    touch apps/$APP/infrastructure/admin.py
    touch apps/$APP/interfaces/__init__.py
    touch apps/$APP/interfaces/views.py
    touch apps/$APP/interfaces/urls.py
    touch apps/$APP/interfaces/forms.py

    echo "  App '$APP' criado."
}

# --- App: accounts ---
create_app_structure accounts
touch apps/accounts/domain/value_objects.py
touch apps/accounts/infrastructure/permissions.py
touch apps/accounts/interfaces/mixins.py

# --- App: employees ---
create_app_structure employees
touch apps/employees/domain/value_objects.py
touch apps/employees/application/use_cases/create_employee.py
touch apps/employees/application/use_cases/update_employee.py
touch apps/employees/application/use_cases/deactivate_employee.py
touch apps/employees/application/use_cases/list_employees.py
touch apps/employees/interfaces/serializers.py

# --- App: documents ---
create_app_structure documents
touch apps/documents/infrastructure/tasks.py
touch apps/documents/application/use_cases/upload_document.py
touch apps/documents/application/use_cases/check_expiring_documents.py
touch apps/documents/interfaces/serializers.py

# --- App: attendance ---
create_app_structure attendance
touch apps/attendance/application/use_cases/register_absence.py
touch apps/attendance/application/use_cases/register_adjustment.py

# --- App: advances ---
create_app_structure advances
touch apps/advances/application/use_cases/create_advance.py
touch apps/advances/application/use_cases/approve_advance.py
touch apps/advances/application/use_cases/reject_advance.py

# --- App: payroll ---
create_app_structure payroll
touch apps/payroll/domain/value_objects.py
touch apps/payroll/application/use_cases/generate_payroll.py
touch apps/payroll/application/use_cases/calculate_termination.py
touch apps/payroll/application/use_cases/generate_payslip.py
touch apps/payroll/infrastructure/tasks.py
touch apps/payroll/interfaces/serializers.py

# --- Templates globais ---
mkdir -p templates/partials
mkdir -p templates/components
mkdir -p templates/dashboard
mkdir -p templates/accounts
mkdir -p templates/employees/partials
mkdir -p templates/documents/partials
mkdir -p templates/attendance/partials
mkdir -p templates/advances/partials
mkdir -p templates/payroll/partials

# Base
touch templates/base.html
touch templates/403.html templates/404.html templates/500.html

# Partials globais
touch templates/partials/navbar.html
touch templates/partials/sidebar.html
touch templates/partials/messages.html
touch templates/partials/pagination.html
touch templates/partials/loading.html
touch templates/partials/confirm_delete.html

# Componentes reutilizáveis
touch templates/components/card.html
touch templates/components/modal.html
touch templates/components/empty_state.html
touch templates/components/badge.html
touch templates/components/stat_card.html

# Dashboard
touch templates/dashboard/index.html

# Accounts
touch templates/accounts/login.html
touch templates/accounts/profile.html
touch templates/accounts/change_password.html
touch templates/accounts/user_list.html
touch templates/accounts/user_form.html

# Employees
touch templates/employees/list.html
touch templates/employees/detail.html
touch templates/employees/form.html
touch templates/employees/entity_list.html
touch templates/employees/entity_form.html
touch templates/employees/farm_list.html
touch templates/employees/farm_form.html
touch templates/employees/jobrole_list.html
touch templates/employees/jobrole_form.html
touch templates/employees/partials/employee_row.html
touch templates/employees/partials/filter_form.html

# Documents
touch templates/documents/list.html
touch templates/documents/form.html
touch templates/documents/detail.html
touch templates/documents/partials/document_row.html

# Attendance
touch templates/attendance/list.html
touch templates/attendance/form.html
touch templates/attendance/partials/attendance_row.html

# Advances
touch templates/advances/list.html
touch templates/advances/form.html
touch templates/advances/detail.html
touch templates/advances/partials/advance_row.html

# Payroll
touch templates/payroll/dashboard.html
touch templates/payroll/payslip.html
touch templates/payroll/termination_form.html
touch templates/payroll/termination_result.html
touch templates/payroll/partials/payroll_summary.html

# --- Static ---
mkdir -p static/css static/js static/images static/fonts
touch static/css/input.css
touch static/css/custom.css
touch static/js/main.js
touch static/js/htmx_config.js

# --- Media ---
mkdir -p media/documents media/photos

# --- Locale ---
mkdir -p locale/pt_BR/LC_MESSAGES

# --- Scripts utilitários ---
mkdir -p scripts
touch scripts/wait_for_db.py
touch scripts/create_superuser.py

echo ""
echo "=========================================="
echo "  Estrutura criada com sucesso!"
echo "=========================================="
echo ""
echo "Total de apps criados: accounts, employees, documents, attendance, advances, payroll"
echo ""
echo "Proximos passos:"
echo "  1. Copie o conteudo de cada arquivo conforme fornecido na conversa"
echo "  2. Configure o arquivo .env baseado no .env.example"
echo "  3. Execute: make build && make up"
echo ""