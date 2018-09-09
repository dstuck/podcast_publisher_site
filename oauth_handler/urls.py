from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^oauth_db', views.oauth_db, name='oauth_db'),
    url(
        r'^oauth-redirect-dev', views.oauth_receiver,
        name='oauth_receiver'
    ),
]
