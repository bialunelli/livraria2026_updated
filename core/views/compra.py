from rest_framework.viewsets import ModelViewSet

from core.models import Compra
from core.serializers.compra import (
    CompraCreateUpdateSerializer,  # ruff: ignore[unused-import]
    CompraListSerializer,  # ruff: ignore[unused-import]
    CompraSerializer,  # ruff: ignore[unused-import]
)


class CompraViewSet(ModelViewSet):
    def get_queryset(self):
        usuario = self.request.user
        if usuario.is_superuser:
            return Compra.objects.all()
        if usuario.groups.filter(name='administradores'):
            return Compra.objects.all()
        return Compra.objects.filter(usuario=usuario)


...
