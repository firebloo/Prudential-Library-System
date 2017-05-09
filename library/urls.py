from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.book_list, name='book_list'),
    url(r'^book/(?P<pk>[0-9]+)/$', views.book_detail, name='book_detail'),
    url(r'^book/new/$', views.book_new, name='book_new'),
    url(r'^book/(?P<pk>[0-9]+)/edit/$', views.book_edit, name='book_edit'),
    url(r'^book/(?P<pk>[0-9]+)/rental/$', views.book_rental, name='book_rental'),
    url(r'^book/(?P<pk>[0-9]+)/release/$', views.book_release, name='book_release'),
]
