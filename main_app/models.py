from django.db import models


class Image(models.Model):
    external_id = models.CharField(max_length=21, unique=True)
    author = models.CharField(max_length=50)
    tags = models.TextField(max_length=300)
    image_file = models.ImageField(upload_to="static/")
