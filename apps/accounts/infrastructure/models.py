from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Usuário customizado do sistema.
    Estende AbstractUser para adicionar perfil de acesso e vínculo com entidade.
    """
    class Role(models.TextChoices):
        ADMIN = "admin", "Administrador"
        HR = "hr", "RH"
        MANAGER = "manager", "Gestor"
        EMPLOYEE = "employee", "Colaborador"

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.EMPLOYEE,
        verbose_name="Perfil de acesso",
    )
    entity = models.ForeignKey(
        "employees.Entity",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users",
        verbose_name="Entidade",
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Telefone",
    )

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"
        ordering = ["first_name", "last_name"]

    def __str__(self):
        return self.get_full_name() or self.username

    @property
    def full_name(self):
        return self.get_full_name() or self.username

    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN or self.is_superuser

    @property
    def is_hr(self):
        return self.role in (self.Role.ADMIN, self.Role.HR) or self.is_superuser

    @property
    def is_manager_or_above(self):
        return self.role in (self.Role.ADMIN, self.Role.HR, self.Role.MANAGER) or self.is_superuser
