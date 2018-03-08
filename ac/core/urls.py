from django.urls import path, include,re_path
from . import views
from django.contrib import admin
from django.conf.urls import url,include


urlpatterns = [
    path('', views.index, name = 'index'),
    path('home/',views.home,name = 'home'),
    path('maps/',views.maps, name = 'maps'),
    path('maps/3dmap',views.mapsd, name = 'mapsd'),
    path('register/',views.signup, name = 'signup'),
    path('accounts/login/', views.loginpage , name = 'loginpage'),
    path('login/validate', views.loginvalidate , name = 'loginvalidate'),
    path('sponsors/', views.sponsors , name = 'sponsors'),
    path('team/', views.team , name = 'team'),
    path('gallery/', views.gallery, name = 'gallery'),
    path('social/', views.social, name = 'social'),
    path('events/', views.events , name = 'events'),
    path('signup/', views.signup , name = 'signup'),
    path('signup/confirm', views.signupconfirm, name = 'signupconfirm'),
    path('secretpath/',views.secret, name = 'secret'),
    path('getqr/',views.test,name ='test'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
]
