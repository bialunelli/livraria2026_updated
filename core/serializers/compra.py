from rest_framework.serializers import CharField, ModelSerializer

from core.models import Compra


class CompraSerializer(ModelSerializer):
    status = CharField(source='get_status_display', read_only=True) # inclua essa linha
    usuario = CharField(source='usuario.email', read_only=True)  # inclua essa linha

    class Meta:
        model = Compra
        fields = '_all_'
