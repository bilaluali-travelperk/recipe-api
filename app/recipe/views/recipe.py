from rest_framework import viewsets
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend


from recipe.models import Recipe
from recipe.serializers import RecipeSerializer
from recipe.filters import RecipeFilter


class RecipeViewSet(viewsets.ModelViewSet):
    """Manage recipes in the database"""
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    filter_backends = (OrderingFilter, DjangoFilterBackend,)
    filterset_class = RecipeFilter
    ordering_fields = ['id', 'name']
    ordering = ['id']
