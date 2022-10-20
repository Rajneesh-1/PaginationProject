from django.db import models


# Create your models here.

class Content(models.Model):
    contentType = models.CharField(max_length=50)
    contentImage = models.URLField()
    contentSpecificName = models.CharField(max_length=50)
