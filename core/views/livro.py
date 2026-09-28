from drf_spectacular.utils import extend_schema  # ruff: ignore[unused-import]
from rest_framework.viewsets import ModelViewSet

from core.models import Livro
from core.serializers import LivroAlterarPrecoSerializer, LivroListSerializer, LivroRetrieveSerializer, LivroSerializer


class LivroViewSet(ModelViewSet):
    queryset = Livro.objects.all()
    serializer_class = LivroSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return LivroListSerializer
        elif self.action == 'retrieve':
            return LivroRetrieveSerializer
        return LivroSerializer

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
