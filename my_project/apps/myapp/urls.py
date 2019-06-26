from django.conf.urls import url
from . import views
                    
urlpatterns = [
    url(r'^$', views.index),
    url(r'^login$',views.login),
    url(r'^signup$',views.signup),
    url(r'^signupp$',views.signupp),
    url(r'^loginp$',views.loginp),
    url(r'^logout$',views.logout),
    url(r'^thelogin$',views.thelogin),
    url(r'^searching$',views.searching),
    url(r'^searching2$',views.searching2),
    
    ]