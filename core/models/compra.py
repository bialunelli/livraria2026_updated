from django.db import models

from .livro import Livro
from .user import User


class Compra(models.Model):
    class TipoPagamento(models.IntegerChoices):
        CARTAO_CREDITO = 1, 'Cartão de Crédito'
        CARTAO_DEBITO = 2, 'Cartão de Débito'
        PIX = 3, 'PIX'
        BOLETO = 4, 'Boleto'
        TRANSFERENCIA_BANCARIA = 5, 'Transferência Bancária'
        CHEQUE = 6, 'Cheque'
        DINHEIRO = 7, 'Dinheiro'
        OUTRO = 8, 'Outro'
    class StatusCompra(models.IntegerChoices):
        CARRINHO = 1, 'Carrinho'
        FINALIZADO = 2, 'Finalizado'
        PAGO = 3, 'Pago'
        ENTREGUE = 4, 'Entregue'

    usuario = models.ForeignKey(User, on_delete=models.PROTECT, related_name='compras')

    status = models.IntegerField(
        choices=StatusCompra.choices,
        default=StatusCompra.CARRINHO
    )

    tipo_pagamento = models.IntegerField(
        choices=TipoPagamento.choices,
        default=TipoPagamento.CARTAO_CREDITO
    )

    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    @property
    def total(self):
        return sum(item.preco * item.quantidade for item in self.itens.all())

    @property
    def total(self):  # ruff: ignore[redefined-while-unused]
        return sum(item.preco * item.quantidade for item in self.itens.all())


class ItensCompra(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE, related_name='itens')
    livro = models.ForeignKey(Livro, on_delete=models.PROTECT, related_name='itens_compra')
    quantidade = models.IntegerField(default=1)
    preco = models.DecimalField(max_digits=7, decimal_places=2, default=0)


class LivroMaisVendidoSerializer(ModelSerializer):
    total_vendidos = IntegerField()

    class Meta:
        model = Livro
        fields = ('id', 'titulo', 'total_vendidos')
