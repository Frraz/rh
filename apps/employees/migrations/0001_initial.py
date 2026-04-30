from django.db import migrations, models
import django.db.models.deletion
import uuid
import simple_history.models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Entity",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ("uuid", models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(db_index=True, default=False)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                ("name", models.CharField(max_length=200, verbose_name="Nome")),
                ("cnpj", models.CharField(blank=True, max_length=18, verbose_name="CNPJ")),
                ("address", models.TextField(blank=True, verbose_name="Endereço")),
                ("phone", models.CharField(blank=True, max_length=20, verbose_name="Telefone")),
                ("email", models.EmailField(blank=True, verbose_name="E-mail")),
                ("is_active", models.BooleanField(default=True, verbose_name="Ativa")),
            ],
            options={"verbose_name": "Entidade", "verbose_name_plural": "Entidades", "ordering": ["name"], "abstract": False},
        ),
        migrations.CreateModel(
            name="Farm",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ("uuid", models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(db_index=True, default=False)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                ("name", models.CharField(max_length=200, verbose_name="Nome")),
                ("city", models.CharField(blank=True, max_length=100, verbose_name="Cidade")),
                ("state", models.CharField(blank=True, max_length=2, verbose_name="UF")),
                ("is_active", models.BooleanField(default=True, verbose_name="Ativa")),
                ("entity", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="farms", to="employees.entity", verbose_name="Entidade")),
            ],
            options={"verbose_name": "Fazenda", "verbose_name_plural": "Fazendas", "ordering": ["entity", "name"], "abstract": False},
        ),
        migrations.CreateModel(
            name="JobRole",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ("uuid", models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(db_index=True, default=False)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                ("name", models.CharField(max_length=100, verbose_name="Nome do Cargo")),
                ("is_active", models.BooleanField(default=True, verbose_name="Ativo")),
                ("entity", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="job_roles", to="employees.entity", verbose_name="Entidade")),
            ],
            options={"verbose_name": "Função", "verbose_name_plural": "Funções", "ordering": ["entity", "name"], "abstract": False},
        ),
        migrations.CreateModel(
            name="Person",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ("uuid", models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(db_index=True, default=False)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                ("person_type", models.CharField(choices=[("employee", "Funcionário CLT"), ("daily", "Diarista")], max_length=10, verbose_name="Tipo")),
                ("status", models.CharField(choices=[("active", "Ativo"), ("inactive", "Inativo")], default="active", max_length=10, verbose_name="Status")),
                ("name", models.CharField(max_length=200, verbose_name="Nome completo")),
                ("cpf", models.CharField(max_length=14, verbose_name="CPF")),
                ("rg", models.CharField(blank=True, max_length=20, verbose_name="RG")),
                ("birth_date", models.DateField(blank=True, null=True, verbose_name="Data de nascimento")),
                ("phone", models.CharField(blank=True, max_length=20, verbose_name="Telefone")),
                ("address", models.TextField(blank=True, verbose_name="Endereço")),
                ("marital_status", models.CharField(blank=True, choices=[("single", "Solteiro(a)"), ("married", "Casado(a)"), ("divorced", "Divorciado(a)"), ("widowed", "Viúvo(a)"), ("other", "Outro")], max_length=10, verbose_name="Estado civil")),
                ("photo", models.ImageField(blank=True, null=True, upload_to="photos/", verbose_name="Foto")),
                ("admission_date", models.DateField(verbose_name="Data de admissão")),
                ("termination_date", models.DateField(blank=True, null=True, verbose_name="Data de demissão")),
                ("pis", models.CharField(blank=True, max_length=20, verbose_name="PIS/PASEP")),
                ("ctps", models.CharField(blank=True, max_length=20, verbose_name="CTPS")),
                ("salary", models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name="Salário (CLT)")),
                ("daily_rate", models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name="Valor da diária")),
                ("bank", models.CharField(blank=True, max_length=100, verbose_name="Banco")),
                ("bank_agency", models.CharField(blank=True, max_length=20, verbose_name="Agência")),
                ("bank_account", models.CharField(blank=True, max_length=30, verbose_name="Conta")),
                ("notes", models.TextField(blank=True, verbose_name="Observações")),
                ("entity", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="persons", to="employees.entity", verbose_name="Entidade")),
                ("farm", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="persons", to="employees.farm", verbose_name="Fazenda")),
                ("job_role", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="persons", to="employees.jobrole", verbose_name="Função")),
            ],
            options={"verbose_name": "Colaborador", "verbose_name_plural": "Colaboradores", "ordering": ["name"], "abstract": False},
        ),
        migrations.AddIndex(
            model_name="person",
            index=models.Index(fields=["entity", "status"], name="employees_p_entity_i_idx"),
        ),
        migrations.AddIndex(
            model_name="person",
            index=models.Index(fields=["person_type", "status"], name="employees_p_person__idx"),
        ),
        migrations.AddIndex(
            model_name="person",
            index=models.Index(fields=["cpf"], name="employees_p_cpf_idx"),
        ),
        migrations.AlterUniqueTogether(
            name="jobrole",
            unique_together={("entity", "name")},
        ),
    ]
