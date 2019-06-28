from django.conf.urls import url
from . import views
                    
urlpatterns = [
    url(r'^$', views.index),
    url(r'^login$',views.login),
    url(r'^signup$',views.signup),
    url(r'^signupp$',views.signupp),
    url(r'^loginp$',views.loginp),
    url(r'^logout$',views.logout),
    url(r'^add$',views.add),
    url(r'^thelogin$',views.thelogin),
    url(r'^searching$',views.searching),
    url(r'^searching2$',views.searching2),
    url(r'^addbrew$', views.addbrew), 
    url(r'^ales$', views.ales), 
    url(r'^malts$', views.malts), 
    url(r'^lagers$', views.lagers), 
    url(r'^stouts$', views.stouts), 
    url(r'^remove/(?P<user_id>\d+)$',views.remove),
    url(r'^fave_beer/(?P<beer_id>\d+)$',views.fave_beer),
    url(r'^show/(?P<beer_id>\d+)$',views.show),
    
    ]