from recipe.models import Recipe


def sample_recipe(**fields):
    """Creates and returns a sample recipe"""
    defaults = {
        'name': 'Sample recipe',
        'description': 'Sample recipe description',
    }
    defaults.update(fields)

    recipe = Recipe.objects.create(**defaults)
    ingredient = {'name': 'Sample ingredient 1'}
    recipe.ingredients.create(**ingredient)

    return recipe


def pick(dict, keys):
    """Build a new dictionary filtering by 'keys'"""
    return {k: dict[k] for k in keys}
