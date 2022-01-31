import django_filters

from recipe.models import Recipe


class RecipeFilter(django_filters.FilterSet):
    """Filters for recipe objects"""
    name = django_filters.CharFilter(lookup_expr='startswith')

    class Meta:
        model = Recipe
        fields = []
