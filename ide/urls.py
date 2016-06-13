"""ide URL Configuration

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
from django.conf.urls import url,include
from django.contrib import admin
from django.views.generic import RedirectView

from page import views as page_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^post$', page_views.post),
    url(r'^history$',page_views.history),
    url(r'^register$',page_views.register),
    url(r'^login$',page_views.login_user),
    url(r'^logout$',page_views.logout_user),
    url(r'^mycodes$',page_views.mycodes),
    #url(r'^ajaxtextpadcall$',page_views.textpad),
    #url(r'^textpad$',page_views.textpad_display),
    url(r'^changepassword$',page_views.change_password),
    url(r'^captcha/', include('captcha.urls')),
    #url(r'^(?P<id>[a-zA-Z0-9]{5})$', page_views.textpad_display),
    url(r'^(?P<id>[a-zA-Z0-9]{6})$', page_views.code_link),
    url(r'^', RedirectView.as_view(url='/post')),       #it redirects to a given url
]
