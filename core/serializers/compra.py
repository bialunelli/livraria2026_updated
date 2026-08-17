from rest_framework.serializers import (
    CharField,
    CurrentUserDefault,
    HiddenField,
    ModelSerializer,
    SerializerMethodField,
)

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


class ItensCompraCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = ItensCompra
        fields = ('livro', 'quantidade')

    def validate_quantidade(self, quantidade):
        if quantidade <= 0:
            raise ValidationError('A quantidade deve ser maior do que zero.')
        return quantidade


class ItensListSerializer(ModelSerializer):
    livro = CharField(source='livro.titulo', read_only=True)

    class Meta:
        model = ItensCompra
        fields = ('quantidade', 'livro')
        depth = 1


class CompraCreateUpdateSerializer(ModelSerializer):
    usuario = HiddenField(default=CurrentUserDefault())
    itens = ItensCompraCreateUpdateSerializer(many=True)  # ruff: ignore[trailing-whitespace]

    class Meta:
        model = Compra
        fields = ('usuario', 'itens')


class CompraSerializer(ModelSerializer):
    status = CharField(source='get_status_display', read_only=True)
    usuario = CharField(source='usuario.email', read_only=True)
    itens = ItensCompraSerializer(many=True, read_only=True)

    class Meta:
        model = Compra
        fields = '_all_'


class CompraListSerializer(ModelSerializer):
    usuario = CharField(source='usuario.email', read_only=True)
    itens = ItensCompraSerializer(many=True, read_only=True)

    class Meta:
        model = Compra
        fields = ('id', 'usuario', 'itens')
