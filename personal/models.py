from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Article(models.Model):
    images = models.ImageField(blank=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=150)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.name