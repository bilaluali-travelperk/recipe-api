from django.test import TestCase
from django.urls import reverse

from rest_framework import status

from recipe.models import Recipe
from recipe.serializers import RecipeSerializer

RECIPES_URL = reverse('recipe:recipe-list')


def sample_recipe(**fields):
    """Creates and returns a sample recipe"""
    defaults = {
        'name': 'Sample recipe',
        'description': 'Sample recipe description'
    }
    defaults.update(fields)

    return Recipe.objects.create(**defaults)


class RecipeApiTests(TestCase):

    def test_list_recipes(self):
        """Test retrieving a list of recipes"""
        sample_recipe()
        sample_recipe()

        res = self.client.get(RECIPES_URL, {'ordering': 'id'})

        recipes = Recipe.objects.all().order_by('id')
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
