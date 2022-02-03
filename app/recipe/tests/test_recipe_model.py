from unittest import TestCase
from recipe import models


class RecipeModelTests(TestCase):

    def test_recipe_str(self):
        """Test the recipe string representation"""
        recipe = models.Recipe.objects.create(
            name="Recipe 1",
            description="Recipe's description 1"
        )

        self.assertEqual(str(recipe), recipe.name)
