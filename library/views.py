from django.shortcuts import render
from django.utils import timezone
from .models import Book
from django.shortcuts import render, get_object_or_404

def book_list(request):
    books = Book.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'library/book_list.html', {'books': books})

def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    Book.objects.get(pk=pk)
    return render(request, 'library/book_detail.html', {'book': book})
   
