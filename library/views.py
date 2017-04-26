from django.shortcuts import render

def book_list(request):
    return render(request, 'library/book_list.html', {})
