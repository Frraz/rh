"""
Model base da camada de infraestrutura.
Fornece campos padrão de auditoria, soft delete e timestamps
para todos os models Django do sistema.
"""
import uuid
from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    """
    Model base com:
    - UUID como identificador público (além do id inteiro do Postgres)
    - Timestamps de criação e atualização automáticos
    - Soft delete (não exclui fisicamente o registro)
    - Campo de auditoria com usuário que criou/alterou
    """
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        verbose_name="UUID",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Criado em",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Atualizado em",
    )
    is_deleted = models.BooleanField(
        default=False,
        verbose_name="Excluído",
        db_index=True,
    )
    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Excluído em",
    )

    class Meta:
        abstract = True

    def soft_delete(self):
        """Marca o registro como excluído sem removê-lo do banco."""
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save(update_fields=["is_deleted", "deleted_at", "updated_at"])

    def restore(self):
        """Restaura um registro marcado como excluído."""
        self.is_deleted = False
        self.deleted_at = None
        self.save(update_fields=["is_deleted", "deleted_at", "updated_at"])


class ActiveManager(models.Manager):
    """Manager padrão que filtra registros não excluídos."""

    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class AllObjectsManager(models.Manager):
    """Manager que retorna todos os registros, incluindo excluídos."""

    def get_queryset(self):
        return super().get_queryset()