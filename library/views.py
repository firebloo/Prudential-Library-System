from django.shortcuts import render
from django.utils import timezone
from .models import Book
from django.shortcuts import render, get_object_or_404
from .forms import BookForm
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from .forms import CreateUserForm
from django.core.urlresolvers import reverse_lazy

def book_list(request):
    books = Book.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'library/book_list.html', {'books': books})

def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    Book.objects.get(pk=pk)
    return render(request, 'library/book_detail.html', {'book': book})

def book_rental(request, pk):
    return redirect('book_detail', pk=pk)

def book_new(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.published_date = timezone.now()
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
          book.published_date = timezone.now()
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