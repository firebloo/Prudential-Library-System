from django.contrib import admin
from .models import Book
from .models import RentHistory

admin.site.register(Book)
admin.site.register(RentHistory)

