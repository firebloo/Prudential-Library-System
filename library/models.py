from django.db import models
from datetime import date
#from django.utils import timezone
from django.contrib.auth.models import User

class Book(models.Model):
    isbn = models.CharField(max_length=13, primary_key=True)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    publisher = models.CharField(max_length=200)
    published_date = models.DateField(blank=False, null=False)
    category = models.CharField(max_length=200)
    page = models.IntegerField()

    request_user = models.CharField(max_length=5, null=True)
    request_date = models.DateField(blank=False, null=False)

    owner_user = models.CharField(max_length=5, null=True)

    def rental(self):
        # self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class RentHistory(models.Model):
    isbn = models.ForeignKey(Book)
    rental_date = models.DateField(blank=False, null=False)
    release_date = models.DateField(blank=False, null=False)
    rental_user = models.ForeignKey(User)

    def rental(self):
        self.rental_date = date.today()
        self.rental_user = User.username
