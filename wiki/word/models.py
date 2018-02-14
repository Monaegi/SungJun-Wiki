from django.db import models


class WikiWord(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()

    def save(self, *args, **kwargs):
        self.title = self.title.lower()
        return super().save(*args, **kwargs)
