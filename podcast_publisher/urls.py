"""podcast_publisher URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from sermon_storer import views as sermon_views

#https://fcc-podcast-handler.herokuapp.com/oauth-redirect-dev
#https://fcc-podcast-handler.herokuapp.com/oauth-redirect-prod
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^oauth/', include('oauth_handler.urls'), name='oauth'),
    url(r'^sermons/', include('sermon_storer.urls'), name='sermons'),
    url(r'^$', sermon_views.index)
]
