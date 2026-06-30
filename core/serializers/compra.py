from core.admin import ItensCompra
from rest_framework.serializers import CharField, ModelSerializer

from core.models import Compra

class ItensCompraSerializer(ModelSerializer):
    class Meta:
        model = ItensCompra
        fields = quantidade



class CompraSerializer(ModelSerializer):
    status = CharField(source='get_status_display', read_only=True)
    usuario = CharField(source='usuario.email', read_only=True)
    itens = ItensCompraSerializer(many=True, read_only=True)

    class Meta:
        model = Compra
        fields = '_all_'
