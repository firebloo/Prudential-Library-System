from django.db import models
from django.utils import timezone

class Book(models.Model):
    isbn = models.CharField(max_length=13)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    publisher = models.CharField(max_length=200)
    published_date = models.DateTimeField(blank=True, null=True)
    category = models.CharField(max_length=200)
    page = models.IntegerField()

    def rental(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
