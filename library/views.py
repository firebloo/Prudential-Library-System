from django.shortcuts import render
from django.utils import timezone
from .models import Book
from .models import RentHistory
from .models import ReserveHistory
from .models import RequestBook
from django.shortcuts import render, get_object_or_404
from .forms import BookForm
from .forms import BookRequestForm
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from .forms import CreateUserForm
from django.urls import reverse_lazy
from datetime import date
from django.contrib import messages
from django.shortcuts import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect

def book_list(request):
    books = Book.objects.filter(published_date__lte=timezone.now()).order_by('-number')
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
    reserve_history = ReserveHistory.objects.filter(isbn=book.isbn).order_by('reserve_date')
    rental_history = RentHistory.objects.filter(isbn=book.isbn).order_by('-rental_date', 'release_date')
    if ReserveHistory.objects.filter(isbn=book.isbn, reserve_user=request.user):
        messages.info(request, '이미 예약중입니다')
        return HttpResponseRedirect('/')
    else:
        ReserveHistory(isbn = book.isbn, reserve_date = date.today(), reserve_user=request.user).save()

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
    books = Book.objects.filter(published_date__lte=timezone.now()).order_by('-number')
    book = get_object_or_404(Book, pk=pk)
    RentHistory(isbn = book.isbn, rental_date = date.today(), rental_user = request.user).save()

    if ReserveHistory.objects.filter(isbn=book.isbn, reserve_user=request.user):
        book_reserve_cancel(request, pk)

    book.rental_user = request.user.username
    book.rental_date = date.today()
    book.save()
    # RentHistory(isbn='123', rental_date=date.today(), release_date=date.today(), rental_user='123').save()
    #Book.objects.get(pk=pk)
    # RentHistory.rental(book, book.isbn) #이게 동작을 안하고 있음.
    return render(request, 'library/book_list.html', {'books': books})

def book_release(request, pk):
    books = Book.objects.filter(published_date__lte=timezone.now()).order_by('-number')
    book = get_object_or_404(Book, pk=pk)
    renthistory = get_object_or_404(RentHistory, isbn=book.isbn, release_date=None)

    renthistory.release_date = date.today()
    renthistory.save()

    book.rental_user = None
    book.rental_date = None
    book.save()
    return render(request, 'library/book_list.html', {'books': books})

def book_request_cancel(request, pk):
    # requestbooks = RequestBook.objects.order_by('request_date')

    requestbook = get_object_or_404(RequestBook, pk=pk)
    requestbook.delete()
    # form = BookRequestForm()
    return redirect('book_request')
    # return render(request, 'library/book_request.html', {'form': form, 'requestbooks': requestbooks})

def book_request(request):
    requestbooks = RequestBook.objects.order_by('request_date')
    if request.method == "POST":
        form = BookRequestForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.request_date = date.today()
            book.request_user = request.user.username
            book.save()
            return redirect('book_request')
    else:
        form = BookRequestForm()
    return render(request, 'library/book_request.html', {'form': form, 'requestbooks':requestbooks})

def book_new_temp(request):
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

def book_new_initialize(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.number = 1
            book.isbn = '9791187345008'
            book.title = '머신 러닝 워크북'
            book.author = '제이슨 벨'
            book.publisher = '길벗'
            book.published_date = '2016-04-30'
            book.category = '전공'
            book.page = 456
            book.request_user = '이성일'
            book.request_date = '2017-01-01'
            book.owner_user = '시스템본부'
            book.save()
            book.number = 2
            book.isbn = '9791186659489'
            book.title = '소프트웨어 장인'
            book.author = '산드로 만쿠소'
            book.publisher = '길벗'
            book.published_date = '2015-09-25'
            book.category = '전공'
            book.page = 328
            book.request_user = '이성일'
            book.request_date = '2017-01-01'
            book.owner_user = '시스템본부'
            book.save()
            book.number = 3
            book.isbn = '9788956608846'
            book.title = '낭만적 연애와 그 후의 일상'
            book.author = '알랭 드 보통'
            book.publisher = '은행나무'
            book.published_date = '2016-08-24'
            book.category = '소설'
            book.page = 300
            book.request_user = '김수민'
            book.request_date = '2017-01-01'
            book.owner_user = '시스템본부'
            book.save()
            book.number = 4
            book.isbn = '9791186274156'
            book.title = '약간의 거리를 둔다'
            book.author = '소노 아야코'
            book.publisher = '책읽는고양이'
            book.published_date = '2016-10-20'
            book.category = '비소설'
            book.page = 160
            book.request_user = '임성준'
            book.request_date = '2017-01-01'
            book.owner_user = '시스템본부'
            book.save()
            book.number = 5
            book.isbn = '9788994120966'
            book.title = '지적 대화를 위한 넓고 얕은 지식 : 현실 세계 편(반양장)'
            book.author = '채사장'
            book.publisher = '한빛비즈'
            book.published_date = '2014-12-04'
            book.category = '비소설'
            book.page = 376
            book.request_user = '임성준'
            book.request_date = '2017-01-01'
            book.owner_user = '시스템본부'
            book.save()
            book.number = 6
            book.isbn = '9788933870693'
            book.title = '설민석의 조선왕조실록'
            book.author = '설민석'
            book.publisher = '도서출판세계사'
            book.published_date = '2016-07-25'
            book.category = '비소설'
            book.page = 504
            book.request_user = '임성준'
            book.request_date = '2017-01-01'
            book.owner_user = '시스템본부'
            book.save()
            book.number = 7
            book.isbn = '9791160486735'
            book.title = '완벽한 공부법'
            book.author = '고영성'
            book.publisher = '로크미디어'
            book.published_date = '2017-01-06'
            book.category = '비소설'
            book.page = 516
            book.request_user = '전종진'
            book.request_date = '2017-01-01'
            book.owner_user = '시스템본부'
            book.save()
            book.number = 8
            book.isbn = '9791187345190'
            book.title = '모두의 라즈베리 파이(Raspberry) with파이썬'
            book.author = '이시이 모루나'
            book.publisher = '길벗'
            book.published_date = '2016-06-13'
            book.category = '전공'
            book.page = 400
            book.request_user = '전명수'
            book.request_date = '2017-01-01'
            book.owner_user = '시스템본부'
            book.save()
            book.number = 9
            book.isbn = '9791195178636'
            book.title = 'CentOS 리눅스 구축관리 실무'
            book.author = '정우영'
            book.publisher = '슈퍼유저코리아'
            book.published_date = '2016-03-01'
            book.category = '전공'
            book.page = 1088
            book.request_user = None
            book.request_date = '2017-01-01'
            book.owner_user = '전명수'
            book.save()
            book.number = 10
            book.isbn = '9788989345909'
            book.title = '실무 전문가가 짚어 주는 UNIX'
            book.author = '조경휘'
            book.publisher = '프리렉'
            book.published_date = '2007-07-26'
            book.category = '전공'
            book.page = 776
            book.request_user = None
            book.request_date = '2017-01-01'
            book.owner_user = '전명수'
            book.save()
            book.number = 11
            book.isbn = '9791185890265'
            book.title = '그림으로 공부하는 IT인프라 구조'
            book.author = '야마자키 야스시'
            book.publisher = '제이펍'
            book.published_date = '2015-07-20'
            book.category = '전공'
            book.page = 384
            book.request_user = None
            book.request_date = '2017-01-01'
            book.owner_user = '전명수'
            book.save()
            book.number = 12
            book.isbn = '9788965401070'
            book.title = '나의 첫 UNIX 교과서'
            book.author = '키모토 마사히코'
            book.publisher = '프리렉'
            book.published_date = '2015-09-08'
            book.category = '전공'
            book.page = 328
            book.request_user = None
            book.request_date = '2017-01-01'
            book.owner_user = '전명수'
            book.save()
            book.number = 13
            book.isbn = '9788956746449'
            book.title = 'Mastering Windows Server 2012 R2'
            book.author = '마크 미나시'
            book.publisher = '정보문화사'
            book.published_date = '2015-10-20'
            book.category = '전공'
            book.page = 1768
            book.request_user = '기존서적'
            book.request_date = '2017-01-01'
            book.owner_user = '시스템본부'
            book.save()
            book.number = 14
            book.isbn = '8979142633'
            book.title = '유닉스 파워 툴 개정 3판'
            book.author = '셀리 파워즈'
            book.publisher = '한빛미디어'
            book.published_date = '2005-01-28'
            book.category = '전공'
            book.page = 1328
            book.request_user = '기존서적'
            book.request_date = '2017-01-01'
            book.owner_user = '시스템본부'
            book.save()
            book.number = 15
            book.isbn = '9788966261024'
            book.title = '테스트 주도 개발'
            book.author = '켄트 벡'
            book.publisher = '인사이트'
            book.published_date = '2014-02-15'
            book.category = '전공'
            book.page = 380
            book.request_user = None
            book.request_date = '2017-01-01'
            book.owner_user = '정민호'
            book.save()
            book.number = 16
            book.isbn = '9788966371358'
            book.title = '세종처럼'
            book.author = '박현모'
            book.publisher = '미다스북스'
            book.published_date = '2014-06-05'
            book.category = '비소설'
            book.page = 464
            book.request_user = None
            book.request_date = '2017-01-01'
            book.owner_user = '김희균'
            book.save()
            book.number = 17
            book.isbn = '8947524204'
            book.title = '피터 드러커의 자기경영 노트'
            book.author = '피터 드러커'
            book.publisher = '한국경제신문사'
            book.published_date = '2003-04-01'
            book.category = '비소설'
            book.page = 254
            book.request_user = None
            book.request_date = '2017-01-01'
            book.owner_user = '김희균'
            book.save()
            book.number = 18
            book.isbn = '9788960861299'
            book.title = '따뜻한 독종'
            book.author = '서거원'
            book.publisher = '위즈덤하우스'
            book.published_date = '2008-09-09'
            book.category = '비소설'
            book.page = 251
            book.request_user = None
            book.request_date = '2017-01-01'
            book.owner_user = '김희균'
            book.save()
            book.number = 19
            book.isbn = '9791157031030'
            book.title = '더 골'
            book.author = '엘리 골드렛'
            book.publisher = '동양북스'
            book.published_date = '2015-08-15'
            book.category = '비소설'
            book.page = 592
            book.request_user = None
            book.request_date = '2017-01-01'
            book.owner_user = '김희균'
            book.save()
            book.number = 20
            book.isbn = '9788997390915'
            book.title = 'Do it! 점프 투 파이썬'
            book.author = '박응용'
            book.publisher = '이지스퍼블리싱'
            book.published_date = '2016-03-03'
            book.category = '전공'
            book.page = 352
            book.request_user = '박찬규'
            book.request_date = '2017-02-01'
            book.owner_user = '시스템본부'
            book.save()
            book.number = 21
            book.isbn = '9788992525701'
            book.title = '언어의 기원'
            book.author = '파스칼 피크'
            book.publisher = '알마'
            book.published_date = '2009-11-02'
            book.category = '비소설'
            book.page = 176
            book.request_user = '이성일'
            book.request_date = '2017-02-01'
            book.owner_user = '시스템본부'
            book.save()
            book.number = 22
            book.isbn = '9788984373068'
            book.title = '브루클린의 소녀'
            book.author = '기욤 뮈소'
            book.publisher = '밝은세상'
            book.published_date = '2016-12-06'
            book.category = '소설'
            book.page = 424
            book.request_user = '김수민'
            book.request_date = '2017-02-01'
            book.owner_user = '시스템본부'
            book.save()
            book.number = 23
            book.isbn = '9788956609959'
            book.title = '종의 기원'
            book.author = '정유정'
            book.publisher = '은행나무'
            book.published_date = '2016-05-14'
            book.category = '소설'
            book.page = 384
            book.request_user = '김수민'
            book.request_date = '2017-02-01'
            book.owner_user = '시스템본부'
            book.save()
            book.number = 24
            book.isbn = '9791195031177'
            book.title = '데이터 시각화, 태블로를 만나다'
            book.author = '솔루젠'
            book.publisher = '솔루젠'
            book.published_date = '2016-12-19'
            book.category = '전공'
            book.page = 204
            book.request_user = '윤일식'
            book.request_date = '2017-02-01'
            book.owner_user = '시스템본부'
            book.save()
            book.number = 25
            book.isbn = '9788968480478'
            book.title = 'Python for Data Analysis'
            book.author = '웨스 맥키니'
            book.publisher = '한빛미디어'
            book.published_date = '2013-10-01'
            book.category = '전공'
            book.page = 592
            book.request_user = '임성준'
            book.request_date = '2017-02-01'
            book.owner_user = '시스템본부'
            book.save()
            book.number = 26
            book.isbn = '9788932473451'
            book.title = '블록 체인 혁명'
            book.author = '돈 탭스콧'
            book.publisher = '을유문화사'
            book.published_date = '2017-01-20'
            book.category = '전공'
            book.page = 588
            book.request_user = '임성준'
            book.request_date = '2017-02-01'
            book.owner_user = '시스템본부'
            book.save()
            book.number = 27
            book.isbn = '9788934939498'
            book.title = '위대한 기업은 다 어디로 갔을까'
            book.author = '짐 콜린스'
            book.publisher = '김영사'
            book.published_date = '2010-07-12'
            book.category = '비소설'
            book.page = 264
            book.request_user = None
            book.request_date = '2017-02-01'
            book.owner_user = '김희균'
            book.save()
            book.number = 28
            book.isbn = '9788965703181'
            book.title = '일을 했으면 성과를 내라'
            book.author = '류랑도'
            book.publisher = '쌤앤파커스'
            book.published_date = '2016-03-23'
            book.category = '비소설'
            book.page = 392
            book.request_user = None
            book.request_date = '2017-02-01'
            book.owner_user = '김희균'
            book.save()
            book.number = 29
            book.isbn = '9788996432517'
            book.title = '성과를 향한 도전'
            book.author = '피터 드러커'
            book.publisher = '간디서원'
            book.published_date = '2010-10-30'
            book.category = '비소설'
            book.page = 280
            book.request_user = None
            book.request_date = '2017-02-01'
            book.owner_user = '김희균'
            book.save()
            book.number = 30
            book.isbn = '9788953128569'
            book.title = '왜 일하는가'
            book.author = '이나모리 가즈오'
            book.publisher = '두란노서원'
            book.published_date = '2017-05-17'
            book.category = '비소설'
            book.page = 240
            book.request_user = None
            book.request_date = '2017-02-01'
            book.owner_user = '김희균'
            book.save()
            book.number = 31
            book.isbn = '9791187038030'
            book.title = '왜 세계의 절반은 굶주리는가?'
            book.author = '장 지글러'
            book.publisher = '갈라파고스'
            book.published_date = '2017-03-31'
            book.category = '비소설'
            book.page = 228
            book.request_user = None
            book.request_date = '2017-02-01'
            book.owner_user = '김희균'
            book.save()
            book.number = 32
            book.isbn = '9780684852867'
            book.title = 'FIRST, BREAK ALL THE RULES'
            book.author = '마커스 버킹엄'
            book.publisher = 'Simon & Schuster'
            book.published_date = '1999-05-05'
            book.category = '비소설'
            book.page = 271
            book.request_user = None
            book.request_date = '2017-02-01'
            book.owner_user = '김희균'
            book.save()
            book.number = 33
            book.isbn = '9788934962984'
            book.title = '어제까지의 세계'
            book.author = '제레드 다이아몬드'
            book.publisher = '김영사'
            book.published_date = '2013-05-09'
            book.category = '비소설'
            book.page = 744
            book.request_user = None
            book.request_date = '2017-02-01'
            book.owner_user = '김희균'
            book.save()
            book.number = 34
            book.isbn = '8820018082551'
            book.title = '백강 고시체 교수'
            book.author = '이태희'
            book.publisher = '백강문자연구원'
            book.published_date = '2008-09-09'
            book.category = '비소설'
            book.page = 218
            book.request_user = '전명수'
            book.request_date = '2017-03-01'
            book.owner_user = '시스템본부'
            book.save()
            book.number = 35
            book.isbn = '9788996817994'
            book.title = 'Oracle, PostgreSQL, MySQL Core Architecture'
            book.author = '권건우'
            book.publisher = '엑셈'
            book.published_date = '2016-12-20'
            book.category = '전공'
            book.page = 322
            book.request_user = '장영천'
            book.request_date = '2017-03-01'
            book.owner_user = '시스템본부'
            book.save()
            book.number = 36
            book.isbn = '9788995932582'
            book.title = '적을 만들지 않는 대화법'
            book.author = '샘 혼'
            book.publisher = '갈매나무'
            book.published_date = '2015-03-23'
            book.category = '비소설'
            book.page = 280
            book.request_user = '김희균'
            book.request_date = '2017-03-01'
            book.owner_user = '시스템본부'
            book.save()
            book.number = 37
            book.isbn = '9788935211463'
            book.title = '인에비터블 미래의 정체'
            book.author = '케빈 켈리'
            book.publisher = '청림출판'
            book.published_date = '2017-01-17'
            book.category = '비소설'
            book.page = 460
            book.request_user = '이광성'
            book.request_date = '2017-03-01'
            book.owner_user = '시스템본부'
            book.save()
            book.number = 38
            book.isbn = '9788931442427'
            book.title = 'DB성능 향상을 위한 SQL Server 운영과 튜닝'
            book.author = 'SQLTAG'
            book.publisher = '영진닷컴'
            book.published_date = '2012-04-17'
            book.category = '전공'
            book.page = 936
            book.request_user = '장영천'
            book.request_date = '2017-03-01'
            book.owner_user = '시스템본부'
            book.save()
            book.number = 39
            book.isbn = '9788997945016'
            book.title = '이장래와 함께하는 SQL Server 2012 운영과 개발'
            book.author = '이장래'
            book.publisher = '아이티포럼'
            book.published_date = '2012-08-25'
            book.category = '전공'
            book.page = 1200
            book.request_user = '전명수'
            book.request_date = '2017-03-01'
            book.owner_user = '시스템본부'
            book.save()
            book.number = 40
            book.isbn = '9788952777867'
            book.title = '플렉서블 씽킹'
            book.author = '마티아스 피셰디크'
            book.publisher = '지식너머'
            book.published_date = '2017-03-25'
            book.category = '비소설'
            book.page = 232
            book.request_user = '전종진'
            book.request_date = '2017-04-01'
            book.owner_user = '시스템본부'
            book.save()
            book.number = 41
            book.isbn = '9788937846243'
            book.title = '풀루언트'
            book.author = '조승연'
            book.publisher = '와이즈베리'
            book.published_date = '2016-10-20'
            book.category = '비소설'
            book.page = 300
            book.request_user = '김희균'
            book.request_date = '2017-04-01'
            book.owner_user = '시스템본부'
            book.save()
            book.number = 42
            book.isbn = '9791156642053'
            book.title = '쉽게 배우는 소프트웨어 공학'
            book.author = '김치수'
            book.publisher = '한빛아카데미'
            book.published_date = '2015-11-30'
            book.category = '전공'
            book.page = 512
            book.request_user = '전명수'
            book.request_date = '2017-04-01'
            book.owner_user = '시스템본부'
            book.save()
            book.number = 43
            book.isbn = '9788970508962'
            book.title = 'R로 배우는 코딩'
            book.author = '장용식'
            book.publisher = '생능출판'
            book.published_date = '2017-01-26'
            book.category = '전공'
            book.page = 404
            book.request_user = '김승빈'
            book.request_date = '2017-04-01'
            book.owner_user = '시스템본부'
            book.save()
            book.number = 44
            book.isbn = '9791159921131'
            book.title = '블록체인 거버먼트'
            book.author = '전명산'
            book.publisher = '알마'
            book.published_date = '2017-05-31'
            book.category = '전공'
            book.page = 312
            book.request_user = '김희균'
            book.request_date = '2017-06-01'
            book.owner_user = '시스템본부'
            book.save()
            book.number = 45
            book.isbn = '9788932317960'
            book.title = '마음'
            book.author = '나쓰메 소세키'
            book.publisher = '현암사'
            book.published_date = '2016-06-25'
            book.category = '소설'
            book.page = 296
            book.request_user = '김희균'
            book.request_date = '2017-06-01'
            book.owner_user = '시스템본부'
            book.save()
            book.number = 46
            book.isbn = '9788937473135'
            book.title = '82년생 김지영'
            book.author = '조남주'
            book.publisher = '민음사'
            book.published_date = '2016-10-14'
            book.category = '소설'
            book.page = 192
            book.request_user = '김수민'
            book.request_date = '2017-06-01'
            book.owner_user = '시스템본부'
            book.save()
            book.number = 47
            book.isbn = '9788937838736'
            book.title = '미스터 하이든'
            book.author = '사샤 아랑고'
            book.publisher = '북폴리오'
            book.published_date = '2016-06-29'
            book.category = '소설'
            book.page = 348
            book.request_user = '김수민'
            book.request_date = '2017-06-01'
            book.owner_user = '시스템본부'
            book.save()
            book.number = 48
            book.isbn = '9788956604992'
            book.title = '7년의 밤'
            book.author = '정유정'
            book.publisher = '은행나무'
            book.published_date = '2011-03-23'
            book.category = '소설'
            book.page = 524
            book.request_user = '김수민'
            book.request_date = '2017-06-01'
            book.owner_user = '시스템본부'
            book.save()
            book.number = 49
            book.isbn = '9788962805901'
            book.title = '클라우스 슈밥의 제4차 산업혁명'
            book.author = '클라우스 슈밥'
            book.publisher = '새로운현재'
            book.published_date = '2016-04-20'
            book.category = '비소설'
            book.page = 288
            book.request_user = '탁근찬'
            book.request_date = '2017-06-01'
            book.owner_user = '시스템본부'
            book.save()
            book.number = 50
            book.isbn = '9788965704119'
            book.title = '리씽크'
            book.author = '스티븐 폴'
            book.publisher = '쌤앤파커스'
            book.published_date = '2017-02-24'
            book.category = '비소설'
            book.page = 400
            book.request_user = '정민호'
            book.request_date = '2017-06-01'
            book.owner_user = '시스템본부'
            book.save()
            book.number = 51
            book.isbn = '9788968482939'
            book.title = '파이썬 웹 프로그래밍 (Django를 활용한 쉽게 빠른 웹 개발, 실전편)'
            book.author = '김석훈'
            book.publisher = '한빛미디어'
            book.published_date = '2016-07-15'
            book.category = '전공'
            book.page = 492
            book.request_user = '박찬규'
            book.request_date = '2017-06-01'
            book.owner_user = '시스템본부'
            book.save()
            book.number = 52
            book.isbn = '9791158390631'
            book.title = '파이썬으로 배우는 알고리즘 트레이딩'
            book.author = '조대표'
            book.publisher = '위키북스'
            book.published_date = '2017-05-17'
            book.category = '전공'
            book.page = 728
            book.request_user = '전명수'
            book.request_date = '2017-06-01'
            book.owner_user = '시스템본부'
            book.save()
            book.number = 53
            book.isbn = '8901103818'
            book.title = '크로스'
            book.author = '정재승/진중권'
            book.publisher = '웅진지식하우스'
            book.published_date = '2009-12-15'
            book.category = '비소설'
            book.page = 336
            book.request_user = '기존서적'
            book.request_date = '2017-06-01'
            book.owner_user = '시스템본부'
            book.save()

            return redirect('book_detail', pk=book.pk)
    else:
        form = BookForm()
    return render(request, 'library/book_edit.html', {'form': form})

def book_new(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.number=54
            book.isbn = '9788960775022'
            book.title = '소프트웨어 테스트 자동화'
            book.author = '도로시 그레이엄'
            book.publisher = '에이콘출판사'
            book.published_date = '2013-12-23'
            book.category = '전공'
            book.page = 728
            book.request_user = '하경호'
            book.request_date = '2017-08-01'
            book.owner_user = '시스템본부'
            book.save()

            book.number=55
            book.isbn = '9788968484636'
            book.title = '밑바닥부터 시작하는 딥러닝'
            book.author = '사이토 고키'
            book.publisher = '한빛미디어'
            book.published_date = '2017-01-03'
            book.category = '전공'
            book.page = 312
            book.request_user = '전명수'
            book.request_date = '2017-08-01'
            book.owner_user = '시스템본부'
            book.save()

            book.number=56
            book.isbn = '9788996731603'
            book.title = 'WebSphere 애플리케이션 아키텍처'
            book.author = '조이 버널'
            book.publisher = 'ISIS'
            book.published_date = '2011-10-06'
            book.category = '전공'
            book.page = 450
            book.request_user = '기존서적'
            book.request_date = '2017-08-01'
            book.owner_user = '시스템본부'
            book.save()

            book.number=57
            book.isbn = '8995848200'
            book.title = '웹 2.0 이노베이션'
            book.author = '오가와 히로시'
            book.publisher = '위즈나인'
            book.published_date = '2006-09-08'
            book.category = '전공'
            book.page = 282
            book.request_user = None
            book.request_date = '2017-08-01'
            book.owner_user = '김성호'
            book.save()

            book.number=58
            book.isbn = '9788994711010'
            book.title = '위험천만 테스팅'
            book.author = '권원일'
            book.publisher = 'STA테스팅컨설팅'
            book.published_date = '2012-06-22'
            book.category = '전공'
            book.page = 145
            book.request_user = None
            book.request_date = '2017-08-01'
            book.owner_user = '김성호'
            book.save()

            book.number=59
            book.isbn = '8970856579'
            book.title = '블루 오션 전략'
            book.author = '김위찬'
            book.publisher = '교보문고'
            book.published_date = '2005-04-08'
            book.category = '비소설'
            book.page = 332
            book.request_user = None
            book.request_date = '2017-08-01'
            book.owner_user = '김성호'
            book.save()

            book.number=60
            book.isbn = '9788956744506'
            book.title = '소프트웨어 요구사항 패턴'
            book.author = '스티브 윗올'
            book.publisher = '정보문화사'
            book.published_date = '2008-10-31'
            book.category = '전공'
            book.page = 520
            book.request_user = None
            book.request_date = '2017-08-01'
            book.owner_user = '김성호'
            book.save()

            book.number=61
            book.isbn = '9788984989603'
            book.title = '생각'
            book.author = '이어령'
            book.publisher = '생각의나무'
            book.published_date = '2009-07-01'
            book.category = '비소설'
            book.page = 280
            book.request_user = None
            book.request_date = '2017-08-01'
            book.owner_user = '김성호'
            book.save()

            book.number=62
            book.isbn = '893491064'
            book.title = '성공하는 기업들의 8가지 습관'
            book.author = '짐 콜린스'
            book.publisher = '김영사'
            book.published_date = '2002-10-10'
            book.category = '비소설'
            book.page = 471
            book.request_user = None
            book.request_date = '2017-08-01'
            book.owner_user = '김성호'
            book.save()

            book.number=63
            book.isbn = '9788996210429'
            book.title = '긍정의 힘'
            book.author = '조엘 오스틴'
            book.publisher = '긍정의힘'
            book.published_date = '2005-05-11'
            book.category = '비소설'
            book.page = 320
            book.request_user = None
            book.request_date = '2017-08-01'
            book.owner_user = '김성호'
            book.save()

            book.number=64
            book.isbn = '8983003995'
            book.title = '한계를 넘어서'
            book.author = '엘리 골드렛'
            book.publisher = '동양북스'
            book.published_date = '2004-10-25'
            book.category = '비소설'
            book.page = 336
            book.request_user = None
            book.request_date = '2017-08-01'
            book.owner_user = '김성호'
            book.save()

            book.number=65
            book.isbn = '8989778980'
            book.title = '경세지략'
            book.author = '홍매'
            book.publisher = '넥서스'
            book.published_date = '2003-11-01'
            book.category = '비소설'
            book.page = 680
            book.request_user = None
            book.request_date = '2017-08-01'
            book.owner_user = '김성호'
            book.save()

            book.number=66
            book.isbn = '9788947527422'
            book.title = '넷브레이킹'
            book.author = '조일훈'
            book.publisher = '한국경제신문사'
            book.published_date = '2010-01-27'
            book.category = '비소설'
            book.page = 286
            book.request_user = None
            book.request_date = '2017-08-01'
            book.owner_user = '김성호'
            book.save()

            book.number=67
            book.isbn = '9788992060257'
            book.title = 'CEO와 경쟁하라'
            book.author = '김도연'
            book.publisher = '토네이도'
            book.published_date = '2007-08-16'
            book.category = '비소설'
            book.page = 264
            book.request_user = None
            book.request_date = '2017-08-01'
            book.owner_user = '김성호'
            book.save()

            book.number=68
            book.isbn = '8990982197'
            book.title = '웹 진화론'
            book.author = '우메다 모치오'
            book.publisher = '도서출판재인'
            book.published_date = '2006-09-16'
            book.category = '비소설'
            book.page = 232
            book.request_user = None
            book.request_date = '2017-08-01'
            book.owner_user = '김성호'
            book.save()

            book.number=69
            book.isbn = '8995398272'
            book.title = '느림에의 초대'
            book.author = '브리깃 뢰트라인'
            book.publisher = '산호와진주'
            book.published_date = '2005-07-15'
            book.category = '비소설'
            book.page = 216
            book.request_user = None
            book.request_date = '2017-08-01'
            book.owner_user = '김성호'
            book.save()

            book.number=70
            book.isbn = '9788961885539'
            book.title = '10미터만 더 뛰어봐!'
            book.author = '김영식'
            book.publisher = '중앙북스'
            book.published_date = '2008-07-01'
            book.category = '비소설'
            book.page = 249
            book.request_user = None
            book.request_date = '2017-08-01'
            book.owner_user = '김성호'
            book.save()

            return redirect('book_detail', pk=book.pk)
    else:
        form = BookForm()
    return render(request, 'library/book_edit.html', {'form': form})

# CBV (Class Based View 작성!)
class CreateUserView(CreateView): # generic view중에 CreateView를 상속받는다.
    template_name = 'registration/signup.html' # 템플릿은?
    form_class =  CreateUserForm # 푸슨 폼 사용? >> 내장 회원가입 폼을 커스터마지징 한 것을 사용하는 경우
    # form_class = UserCreationForm >> 내장 회원가입 폼 사용하는 경우
    success_url = reverse_lazy('create_user_done') # 성공하면 어디로?

class RegisteredView(TemplateView): # generic view중에 TemplateView를 상속받는다.
    template_name = 'registration/signup_done.html' # 템플릿은?

