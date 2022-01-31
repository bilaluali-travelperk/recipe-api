from rest_framework import viewsets
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend


from recipe.models import Recipe
from recipe.serializers import RecipeSerializer, RecipeDetailSerializer
from recipe.filters import RecipeFilter


class RecipeViewSet(viewsets.ModelViewSet):
    """Manage recipes in the database"""
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    filter_backends = (OrderingFilter, DjangoFilterBackend,)
    filterset_class = RecipeFilter
    ordering_fields = ['id', 'name']
    ordering = ['id']

    def get_serializer_class(self):
        return {
            'retrieve': RecipeDetailSerializer,
        }.get(self.action, self.serializer_class)
