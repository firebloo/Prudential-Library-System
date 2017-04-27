from django.shortcuts import render
from django.utils import timezone
from .models import Book

def book_list(request):
    books = Book.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'library/book_list.html', {'books': books})
