from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField( max_length=250)
    slug = models.SlugField(max_length=250)
    
    def __str__(self) -> str:
        return self.name