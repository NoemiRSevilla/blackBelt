from django.conf.urls import url
from . import views
                    
urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^quotes$', views.quotes),
    url(r'^quotes/(?P<quote_id>\d+)/like$', views.likes),
    url(r'^quotes/(?P<quote_id>\d+)/unlike$', views.unlikes),

    url(r'^myaccount/(?P<user_id>\d+)$', views.edit),
    url(r'^user/(?P<user_id>\d+)$', views.show),
    url(r'^quotes/(?P<quote_id>\d+)/delete$', views.delete)
]