from django.db import models
from register.models import User

class Shop(models.Model):
    """ お店情報を持つmodel """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True)
    eyecatch_image = models.ImageField(upload_to='images', blank=True, null=True)
    name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=15)
    access = models.CharField(max_length=30)
    buisiness_time1 = models.CharField(max_length=30)
    buisiness_time2 = models.CharField(max_length=30)
    non_buisiness_day = models.CharField(max_length=30)
    seats = models.CharField(max_length=3)
    park = models.CharField(max_length=30)
    youtube_url = models.CharField(max_length=100)
    twitter_id = models.CharField(max_length=100)
    twitter_url = models.URLField(max_length=100)
    greeting = models.TextField(max_length=500)

    def __str__(self):
        return self.name
    
    