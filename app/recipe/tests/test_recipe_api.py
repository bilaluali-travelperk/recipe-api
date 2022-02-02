from django.test import TestCase
from django.urls import reverse

from rest_framework import status

from recipe.models import Recipe
from recipe.serializers import RecipeSerializer


def recipe_url(pattern, args=[]):
    return reverse(f'recipe:recipe-{pattern}', args=args)


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
        }

        url = recipe_url('list')
        res = self.client.post(url, data)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        res_data = {k: res.data[k] for k in data.keys()}
        self.assertEqual(data, res_data)

    def test_patch_recipe(self):
        """Test updating a recipe with patch"""
        recipe = sample_recipe()
        data = {
            'name': 'Updated recipe name',
            'description': 'Updated recipe description',
        }

        url = recipe_url('detail', [recipe.id])
        res = self.client.patch(url, data,
                                content_type='application/json')

        recipe.refresh_from_db()
        serializer = RecipeSerializer(recipe)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_patch_recipe_name(self):
        """Test updating name of a recipe with patch"""
        recipe = sample_recipe()
        data = {
            'name': 'Updated recipe name',
        }

        url = recipe_url('detail', [recipe.id])
        res = self.client.patch(url, data,
                                content_type='application/json')

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
        res = self.client.patch(url, data,
                                content_type='application/json')

        recipe.refresh_from_db()
        serializer = RecipeSerializer(recipe)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_delete_recipe(self):
        """Test deleting recipe"""
        recipe = sample_recipe()
        sample_recipe()
        sample_recipe()

        url = recipe_url('detail', [recipe.id])
        res = self.client.delete(url)

        recipes_ids = Recipe.objects.all().values_list('id', flat=True)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertNotIn(recipe.id, recipes_ids)
