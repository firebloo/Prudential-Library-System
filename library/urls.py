from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.book_list, name='book_list'),
    url(r'^book/(?P<pk>[0-9]+)/$', views.book_detail, name='book_detail'),
    url(r'^book/new/$', views.book_new, name='book_new'),
    url(r'^book/(?P<pk>[0-9]+)/edit/$', views.book_edit, name='book_edit'),
    url(r'^book/(?P<pk>[0-9]+)/rental/$', views.book_rental, name='book_rental'),
    url(r'^book/(?P<pk>[0-9]+)/release/$', views.book_release, name='book_release'),
    url(r'^book/(?P<pk>[0-9]+)/reserve/$', views.book_reserve, name='book_reserve'),
    url(r'^book/(?P<pk>[0-9]+)/reserve_cancel/$', views.book_reserve_cancel, name='book_reserve_cancel'),
    url(r'^book/request/$', views.book_request, name='book_request'),
    # url(r'^book/request_cancel/$', views.book_request_cancel, name='book_request_cancel'),
    url(r'^book/request_cancel/(?P<pk>[0-9]*)', views.book_request_cancel, name='book_request_cancel'),
    url('^change-password/done/$', views.book_list, name='password_change_done'),
]
