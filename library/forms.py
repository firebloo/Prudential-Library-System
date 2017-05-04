from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from .models import Book

class BookForm(forms.ModelForm):
  
    class Meta:
        model = Book
        fields = ('title', 'author',)


class CreateUserForm(UserCreationForm): # 내장 회원가입 폼을 상속받아서 확장한다.
    email = forms.EmailField(required=True) # 이메일 필드 추가
    dept = forms.ComboField('시스템운영팀')
    #['시스템개발팀', '시스템운영팀', '시스템기획팀', '정보보호팀']

    class Meta:
        model = User
        fields = ("dept", "username", "email", "password1", "password2")

    def save(self, commit=True): # 저장하는 부분 오버라이딩
        user = super(CreateUserForm, self).save(commit=False) # 본인의 부모를 호출해서 저장하겠다.
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
