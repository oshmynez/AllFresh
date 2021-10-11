from django.db import models


# Create your models here.


class Article(models.Model):
    title = models.CharField(max_length=200)
    imageUrl = models.URLField()
    category = models.CharField(max_length=40,default='')
    datePublication = models.DateField()
    articleUrl = models.URLField(blank=True)

    def __str__(self):
        return self.title