from rest_framework import viewsets, filters

from recipe.models import Recipe
from recipe.serializers import RecipeSerializer, RecipeDetailSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    """Manage recipes in the database"""
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['id', 'name']
    ordering = ['id']

    def get_serializer_class(self):
        return {
            'retrieve': RecipeDetailSerializer,
        }.get(self.action, self.serializer_class)
