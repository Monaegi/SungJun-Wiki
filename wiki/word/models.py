from django.db import models


class WikiWord(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
