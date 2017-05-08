from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from .models import Book

class BookForm(forms.ModelForm):
  
    class Meta:
        model = Book
        fields = ('isbn', 'title', 'author', 'publisher', 'category', 'page', )


class CreateUserForm(UserCreationForm): # 내장 회원가입 폼을 상속받아서 확장한다.
    SOP = '시스템운영팀'
    SYD = '시스템개발팀'
    ISC = '정보보호팀'
    SYP = '시스템기획팀'
    dept_choices = ((SOP, "시스템운영팀"),
                    (SYD, "시스템개발팀"),
                    (ISC, "정보보호팀"),
                    (SYP, "시스템기획팀"),
                    )
    dept = forms.ChoiceField(choices=dept_choices)

    class Meta:
        model = User
        fields = ("dept", "username", "password1", "password2")

    def save(self, commit=True): # 저장하는 부분 오버라이딩
        user = super(CreateUserForm, self).save(commit=False) # 본인의 부모를 호출해서 저장하겠다.
        if commit:
            user.save()
        return user
