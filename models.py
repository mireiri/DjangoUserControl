from django.db import models
from django.contrib.auth import get_user_model


class Triplog(models.Model):
    
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        ) 
    
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=200)
    latitude = models.CharField(max_length=50)
    longitude = models.CharField(max_length=50)
    create_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title
