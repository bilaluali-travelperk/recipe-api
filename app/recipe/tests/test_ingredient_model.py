from unittest import TestCase
from recipe import models

from .helpers import sample_recipe


class IngredientModelTests(TestCase):

    def test_ingredient_str(self):
        """Test the ingredient string representation"""
        ingredient = models.Ingredient.objects.create(
            name="Ingredient 1",
            recipe=sample_recipe()
        )

        self.assertEqual(str(ingredient), ingredient.name)
