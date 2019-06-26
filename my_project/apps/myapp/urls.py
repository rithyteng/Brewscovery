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
<<<<<<< HEAD
    url(r'^searching$',views.searching),
    url(r'^searching2$',views.searching2),
=======
>>>>>>> 1548ee2665fb10a75ff43d3324ed8f848ccf43c1
]