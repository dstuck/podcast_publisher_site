from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

app_name='sermons'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login', auth_views.LoginView.as_view(
        template_name='login.html'
    ), name='login'),
   # url(r'^login', views.login, name='login'),
    url(r'^update', views.update_from_ftp, name='update'),
]
