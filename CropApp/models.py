from django.db import models
from utils.image_rename import *


class CropsCategoryModel(models.Model):
    title = models.CharField(max_length=355, help_text="Crops category name")
    image = models.ImageField(upload_to=crops_category_image,
                              null=True, blank=True, help_text="Crops category image")

    class Meta:
        db_table = 'crops_categories'

    def __str__(self) -> str:
        return self.title


class DiseasesModel(models.Model):
    """
    Diseases model represents to diseases instance with name and image
    """
    title = models.CharField(max_length=355, help_text="Diseases name")
    image = models.ImageField(upload_to=crops_disease_image, null=True, blank=True,
                              help_text="Diseases image")
    # user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_diseases')

    class Meta:
        db_table = 'diseases'

    def __str__(self) -> str:
        return self.title


class CropsModel(models.Model):
    title = models.CharField(max_length=355, help_text="Crops name")
    disease = models.ManyToManyField(
        DiseasesModel, related_name='crops_diseases')
    category = models.ForeignKey(
        CropsCategoryModel, on_delete=models.CASCADE, related_name='crops_categories')
    image = models.ImageField(upload_to=crops_image,
                              null=True, blank=True, help_text="Crops image")
    description = models.TextField(
        blank=True, null=True, help_text="Crops description")
    is_archived = models.BooleanField(default=False)

    class Meta:
        db_table = 'crops'

    def __str__(self) -> str:
        return self.title
