from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from django.conf import settings
from django.views.generic.base import RedirectView
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    #
    path('index/', views.home, name='index'),
    path('', RedirectView.as_view(url='index')),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('signup/', views.signup_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('contact/', views.contact_view, name='contact'),
    path('about/', views.about_view, name='about'),

    # path('Profile/edit/<int:pk>', views.ProfileUpdateView.as_view(success_url='/app1/index')),

]
