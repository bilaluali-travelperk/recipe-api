from django.db import models


class Ingredient(models.Model):
    """Ingredient object"""
    name = models.CharField(max_length=255)
    recipe = models.ForeignKey(
        'Recipe',
        on_delete=models.CASCADE,
        related_name="ingredients",
        related_query_name="ingredient",
    )

    def __str__(self):
        return self.name
