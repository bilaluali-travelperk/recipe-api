from recipe.models import Recipe, Ingredient


def sample_recipe(**fields):
    """Creates and returns a sample recipe"""
    defaults = {
        'name': 'Sample recipe',
        'description': 'Sample recipe description'
    }
    defaults.update(fields)

    return Recipe.objects.create(**defaults)


def sample_ingredient(**fields):
    """Creates and returns a sample ingredient"""
    defaults = {
        'name': 'Sample ingredient',
        'recipe': sample_recipe()
    }
    defaults.update(fields)

    return Ingredient.objects.create(**defaults)
