from django.test import TestCase
from django.urls import reverse
from copy import copy

from rest_framework import status

from recipe.models import Recipe, Ingredient
from recipe.serializers import RecipeSerializer
from .helpers import sample_recipe, pick


def recipe_url(pattern, args=[]):
    return reverse(f'recipe:recipe-{pattern}', args=args)


class RecipeApiTests(TestCase):

    def test_list_recipes(self):
        """Test retrieving a list of recipes"""
        sample_recipe()
        sample_recipe()

        url = recipe_url('list')
        res = self.client.get(url, {'ordering': 'id'})

        recipes = Recipe.objects.all().order_by('id')
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_list_recipes_startswith_name(self):
        """Test retrieving a list of recipes starting with param
        substring name"""
        substr = 'Baked'
        sample_recipe(name=f'{substr} Spaghetti')
        sample_recipe(name=f'{substr} Mushroom')
        sample_recipe(name=f'{substr} Chciken')
        sample_recipe(name=f'Does not start with {substr}')

        url = recipe_url('list')
        res = self.client.get(url, {
            'ordering': 'id',
            'name': substr
        })

        recipes = Recipe.objects \
            .filter(name__startswith=substr) \
            .order_by('id')
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_detail_recipe(self):
        """Test retrieving a detailed recipe"""
        recipe = sample_recipe()

        url = recipe_url('detail', [recipe.id])
        res = self.client.get(url)

        serializer = RecipeSerializer(recipe)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_detail_undefined_recipe(self):
        """Test retrieving a non existing recipe"""
        url = recipe_url('detail', ['undefinedId'])
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_recipe(self):
        """Test creating a simple recipe"""
        data = {
            'name': 'Test recipe 1',
            'description': 'Test recipe 1 description',
            'ingredients': []
        }

        url = recipe_url('list')
        content_type = 'application/json'
        res = self.client.post(url, data, content_type=content_type)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            pick(res.data, ['name', 'description']),
            pick(data, ['name', 'description'])
        )

    def test_create_recipe_with_ingredients(self):
        """Test creating a recipe with ingredients"""
        data = {
            'name': 'Test recipe 1',
            'description': 'Test recipe 1 description',
            'ingredients': [
                {'name': 'Test ingredient 1'},
                {'name': 'Test ingredient 2'},
            ]
        }

        url = recipe_url('list')
        content_type = 'application/json'
        res = self.client.post(url, data, content_type=content_type)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            pick(res.data, ['name', 'description']),
            pick(data, ['name', 'description'])
        )

        ingredients = [pick(ingredient, ['name'])
                        for ingredient in res.data['ingredients']]

        self.assertEqual(len(ingredients), len(data['ingredients']))
        self.assertEqual(ingredients, data['ingredients'])

    def test_create_bad_recipe(self):
        """Test creating a recipe with missing params"""
        data = {
            'name': 'Test recipe 1',
            'description': 'Test recipe 1 description',
        }

        url = recipe_url('list')
        content_type = 'application/json'
        res = self.client.post(url, data, content_type=content_type)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_recipe_name(self):
        """Test updating name of a recipe with patch"""
        recipe = sample_recipe()
        data = {
            'name': 'Updated recipe name',
        }

        url = recipe_url('detail', [recipe.id])
        content_type = 'application/json'
        res = self.client.patch(url, data, content_type=content_type)

        recipe.refresh_from_db()
        serializer = RecipeSerializer(recipe)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_patch_recipe_description(self):
        """Test updating description of a recipe with patch"""
        recipe = sample_recipe()
        data = {
            'description': 'Updated recipe description',
        }

        url = recipe_url('detail', [recipe.id])
        content_type = 'application/json'
        res = self.client.patch(url, data, content_type=content_type)

        recipe.refresh_from_db()
        serializer = RecipeSerializer(recipe)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_patch_recipe_ingredients(self):
        """Test updating recipe's ingredients with patch"""
        recipe = sample_recipe()
        data = {
            'ingredients': [
                {'name': 'Updated ingredient 1'},
                {'name': 'Updated ingredient 2'},
            ]
        }

        ingredients = recipe.ingredients
        ingredients_ids_delete = copy(ingredients.values('id'))

        url = recipe_url('detail', [recipe.id])
        content_type = 'application/json'
        res = self.client.patch(url, data, content_type=content_type)

        recipe.refresh_from_db()
        serializer = RecipeSerializer(recipe)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

        ingredients_ids = Ingredient.objects.all().values('id')
        for id in ingredients_ids_delete:
            self.assertNotIn(id, ingredients_ids)

    def test_delete_recipe(self):
        """Test deleting recipe"""
        recipe = sample_recipe()
        sample_recipe()
        sample_recipe()

        url = recipe_url('detail', [recipe.id])
        res = self.client.delete(url)

        recipes_ids = Recipe.objects.all().values('id')

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertNotIn(recipe.id, recipes_ids)
