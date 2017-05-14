from django.shortcuts import render
from django.utils import timezone
from .models import Book
from .models import RentHistory
from .models import ReserveHistory
from django.shortcuts import render, get_object_or_404
from .forms import BookForm
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from .forms import CreateUserForm
from django.core.urlresolvers import reverse_lazy
from datetime import date

def book_list(request):
    books = Book.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    rental_history = RentHistory.objects.filter(release_date__isnull = True)
    return render(request, 'library/book_list.html', {'books': books, 'rental_history': rental_history})

def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    Book.objects.get(pk=pk)
    reserve_history = ReserveHistory.objects.filter(isbn=book.isbn).order_by('-reserve_date', 'reserve_user')
    rental_history = RentHistory.objects.filter(isbn=book.isbn).order_by('-rental_date', 'release_date')
    return render(request, 'library/book_detail.html', {'book': book, 'rental_history': rental_history,
                                                        'reserve_history': reserve_history})

def book_reserve(request, pk):
    book = get_object_or_404(Book, pk=pk)
    ReserveHistory(isbn = book.isbn, reserve_date = date.today(), reserve_user=request.user).save()
    reserve_history = ReserveHistory.objects.filter(isbn=book.isbn).order_by('-reserve_date', 'reserve_user')
    rental_history = RentHistory.objects.filter(isbn=book.isbn).order_by('-rental_date', 'release_date')
    return render(request, 'library/book_detail.html', {'book': book, 'rental_history': rental_history,
                                                        'reserve_history': reserve_history})

def book_reserve_cancel(request, pk):
    book = get_object_or_404(Book, pk=pk)
    reservehistory = get_object_or_404(ReserveHistory, reserve_user=request.user.username, isbn=book.isbn)
    reservehistory.delete()
    reserve_history = ReserveHistory.objects.filter(isbn=book.isbn).order_by('-reserve_date', 'reserve_user')
    rental_history = RentHistory.objects.filter(isbn=book.isbn).order_by('-rental_date', 'release_date')
    return render(request, 'library/book_detail.html', {'book': book, 'rental_history': rental_history,
                                                        'reserve_history': reserve_history})

def book_rental(request, pk):
    books = Book.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    book = get_object_or_404(Book, pk=pk)
    RentHistory(isbn = book.isbn, rental_date = date.today(), rental_user = request.user).save()
    book.rental_user = request.user.username
    book.rental_date = date.today()
    book.save()
    # RentHistory(isbn='123', rental_date=date.today(), release_date=date.today(), rental_user='123').save()
    #Book.objects.get(pk=pk)
    # RentHistory.rental(book, book.isbn) #이게 동작을 안하고 있음.
    return render(request, 'library/book_list.html', {'books': books})

def book_release(request, pk):
    books = Book.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    book = get_object_or_404(Book, pk=pk)
    renthistory = get_object_or_404(RentHistory, isbn=book.isbn, release_date=None)

    renthistory.release_date = date.today()
    renthistory.save()

    book.rental_user = None
    book.rental_date = None
    book.save()
    return render(request, 'library/book_list.html', {'books': books})

def book_new(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            # book.published_date = timezone.now()
            # book.publisher = "Me"
            # book.isbn = '12345'
            # book.category = 'none'
            # book.page = 350
            book.save()
            return redirect('book_detail', pk=book.pk)
    else:
        form = BookForm()
    return render(request, 'library/book_edit.html', {'form': form})   

def book_edit(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
      form = BookForm(request.POST, instance=book)
      if form.is_valid():
          book = form.save(commit=False)
          # book.published_date = timezone.now()
          # book.publisher = "Me"
          # book.isbn = '12345'
          # book.category = 'none'
          # book.page = 350
          book.save()
          return redirect('book_detail', pk=book.pk)
    else:
        form = BookForm(instance=book)
    return render(request, 'library/book_edit.html', {'form': form})


# CBV (Class Based View 작성!)
class CreateUserView(CreateView): # generic view중에 CreateView를 상속받는다.
    template_name = 'registration/signup.html' # 템플릿은?
    form_class =  CreateUserForm # 푸슨 폼 사용? >> 내장 회원가입 폼을 커스터마지징 한 것을 사용하는 경우
    # form_class = UserCreationForm >> 내장 회원가입 폼 사용하는 경우
    success_url = reverse_lazy('create_user_done') # 성공하면 어디로?

class RegisteredView(TemplateView): # generic view중에 TemplateView를 상속받는다.
    template_name = 'registration/signup_done.html' # 템플릿은?