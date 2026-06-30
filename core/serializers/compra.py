from rest_framework.serializers import CharField, ModelSerializer, SerializerMethodField

from core.models import Compra, ItensCompra


class ItensCompraSerializer(ModelSerializer):
    titulo = CharField(source='livro.titulo', read_only=True)
    editora = CharField(source='livro.editora.nome', read_only=True)
    preco = CharField(source='livro.preco', read_only=True)
    capa = CharField(source='livro.capa.url', read_only=True)

    total = SerializerMethodField()

    def get_total(self, item):
        return item.livro.preco * item.quantidade

    class Meta:
        model = ItensCompra
        fields = {'titulo', 'quantidade', 'preco', 'capa', 'editora'}
        depth = 1


class CompraSerializer(ModelSerializer):
    status = CharField(source='get_status_display', read_only=True)
    usuario = CharField(source='usuario.email', read_only=True)
    itens = ItensCompraSerializer(many=True, read_only=True)

    class Meta:
        model = Compra
        fields = '_all_'
