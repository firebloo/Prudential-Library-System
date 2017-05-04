from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from library import views as library_views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'', include('library.urls')),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^signup/$', library_views.CreateUserView.as_view(), name = 'signup'),
    url(r'^signup_done/$', library_views.RegisteredView.as_view(), name = 'create_user_done'),
    #url(r'^accounts/', include('django.contrib.auth.urls')),
]
