from django.contrib import admin
from django.urls import path, include
from home import views


urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('search', views.search, name='search'),
    path('settings', views.settings, name='settings'),
    path('userPreference', views.userPreference, name='userPreference'),
    path('signup/', views.signup, name='signup'),
    path("email/verify/<token>",views.verifyemail),
    path('confirmUser/', views.confirmUser, name='confirmUser'),
    path('checkUser/', views.checkUser, name='checkUser'),
    path('profile/', views.profile, name='profile'),
    path('editProfile/', views.editProfile, name='editProfile'),
    path('changepassword/', views.changepassword, name='changepassword'),
    path('signIn/', views.handlelogin, name='handlelogin'),
    path('logout', views.handlelogout, name='handlelogout'),
    path('base/', views.base, name="base"),
]
