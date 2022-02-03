from rest_framework import serializers

from recipe.models import Recipe, Ingredient


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for ingredient objects"""

    class Meta:
        model = Ingredient
        fields = ('id', 'name',)
        read_only_fields = ('id',)


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipe objects"""
    ingredients = IngredientSerializer(many=True)

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'description', 'ingredients',)
        read_only_fields = ('id',)

    def create(self, data):
        """Handles how child relationships (ingredients)
        should be saved"""
        ingredients = data.pop('ingredients')
        recipe = Recipe.objects.create(**data)

        for ingredient in ingredients:
            recipe.ingredients.create(**ingredient)

        return recipe

    def update(self, instance, data):
        """Handles how child relationships (ingredients)
        should be updated"""
        if 'ingredients' in data.keys():
            ingredients_data = data.pop('ingredients')
            ingredients_to_delete = instance.ingredients.values('id')

            Ingredient.objects.filter(id__in=ingredients_to_delete).delete()

            for ingredient in ingredients_data:
                instance.ingredients.create(**ingredient)

        Recipe.objects.filter(id=instance.id).update(**data)
        instance.refresh_from_db()

        return instance
