from django.db import models
from django.conf import settings


def upload_path_handler(instance, filename):
    return "images/ingredients/{name}/{file}".format(
        name=instance.name, file=filename
    )

class Ingredient(models.Model):
    name        = models.CharField(max_length = 50)
    image       = models.ImageField(upload_to = upload_path_handler)

    def __str__(self):
        return self.name

def upload_path_handler(instance, filename):
    return "images/recipes/{label}/{file}".format(
        label=instance.label, file=filename
    )

class Recipe(models.Model):
    createdBy          = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete = models.CASCADE, related_name='recipe_user')
    label              = models.CharField(max_length=50)
    instructions       = models.TextField(max_length=255)
    totalTime          = models.TimeField()
    url                = models.URLField(null=True)
    image              = models.ImageField(upload_to = upload_path_handler)
    healthLabels       = models.JSONField()
    totalNutrients     = models.JSONField()
    calories           = models.IntegerField()
    cuisineType        = models.CharField(max_length=50)
    mealType           = models.CharField(max_length=50)
    dishType           = models.CharField(max_length=50)
    likes              = models.PositiveIntegerField(default = 0)
    missingIngredients = models.JSONField(null = True)

    def __str__(self):
        return self.label

class IngredientList(models.Model):
    recipe          = models.ForeignKey(Recipe,on_delete=models.CASCADE,related_name='ingredient_list')
    ingredient      = models.ForeignKey(Ingredient,on_delete=models.CASCADE,related_name='recipe_ingredient')
    quantity        = models.FloatField(default = 1.0)

    def __str__(self):
        return f"{self.ingredient} - {self.quantity}"

class Likes(models.Model):
    user            = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete = models.CASCADE, related_name='user_likes')
    recipe          = models.ForeignKey(Recipe,on_delete=models.CASCADE,related_name='recipe_likes')

    class Meta:
        verbose_name_plural = 'Likes'

    def __str__(self):
        return f"{self.recipe} by {self.user}"

class Favourite(models.Model):
    user            = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete = models.CASCADE, related_name='user_fav')
    recipe          = models.ForeignKey(Recipe,on_delete=models.CASCADE,related_name='recipe_fav')

    def __str__(self):
        return f"{self.recipe} for {self.user}"

class Inventory(models.Model):
    user            = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete = models.CASCADE, related_name='user_inventory')
    ingredient      = models.ForeignKey(Ingredient,on_delete=models.CASCADE,related_name='inventory_ingredient')
    quantity        = models.FloatField(default = 1.0)

    class Meta:
        verbose_name_plural = 'Inventories'
    
    def __str__(self):
        return f"{self.ingredient} - {self.quantity}"

class ShoppingList(models.Model):
    user            = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete = models.CASCADE, related_name='user_shopping_list')
    ingredient      = models.ForeignKey(Ingredient,on_delete=models.CASCADE,related_name='list_ingredient')
    quantity        = models.FloatField(default = 1.0)
    
    def __str__(self):
        return f"{self.ingredient} - {self.quantity}"

class DietLog(models.Model):
    user            = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete = models.CASCADE, related_name='user_log')
    recipe          = models.ForeignKey(Recipe,on_delete=models.CASCADE,related_name='recipe_log')
    date            = models.DateField(auto_now_add=True)
    calories        = models.FloatField(default = 0)
    cholestrol      = models.FloatField(default = 0)
    fat             = models.FloatField(default = 0)
    sugar           = models.FloatField(default = 0)
    proteins        = models.FloatField(default = 0)

    def __str__(self):
        return f"{self.user} on {self.date}"