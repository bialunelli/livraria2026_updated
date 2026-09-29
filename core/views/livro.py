from drf_spectacular.utils import extend_schema  # ruff: ignore[unused-import]
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from core.models import Livro
from core.serializers import LivroAlterarPrecoSerializer, LivroListSerializer, LivroRetrieveSerializer, LivroSerializer


class LivroViewSet(ModelViewSet):
    queryset = Livro.objects.all()
    serializer_class = LivroSerializer

    @action(detail=False, methods=['get'])
        def mais_vendidos(self, request):
            livros = Livro.objects.annotate(
                total_vendidos=Sum(
                    'itens_compra__quantidade',
                    filter=Q(itens_compra__compra__status=Compra.StatusCompra.FINALIZADO)
                )
            ).filter(total_vendidos__gt=10).order_by('-total_vendidos')

            serializer = LivroMaisVendidoSerializer(livros, many=True)

            if not serializer.data:
                return Response(
                    {"detail": "Nenhum livro excedeu 10 vendas."},
                    status=status.HTTP_200_OK
                )

            return Response(serializer.data, status=status.HTTP_200_OK)

    def get_serializer_class(self):
        if self.action == 'list':
            return LivroListSerializer
        elif self.action == 'retrieve':
            return LivroRetrieveSerializer
        return LivroSerializer

    @extend_schema(
        request=LivroAlterarPrecoSerializer,
        responses={200: None},
        description="Altera o preço de um livro específico.",
        summary="Alterar preço do livro",
    )
    @action(detail=True, methods=['patch'])  # ruff: ignore[undefined-name]
    def alterar_preco(self, request, pk=None):
        livro = self.get_object()

        serializer = LivroAlterarPrecoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        livro.preco = serializer.validated_data['preco']
        livro.save()

        return Response(  # ruff: ignore[undefined-name]
            {'detail': f'Preço do livro "{livro.titulo}" atualizado para {livro.preco}.'}, status=status.HTTP_200_OK  # ruff: ignore[undefined-name]
        )
