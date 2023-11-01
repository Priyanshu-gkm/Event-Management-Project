from django.contrib import admin
from django.urls import path , include
from accounts import views

urlpatterns = [
    path("accounts/",include('accounts.urls')),
    path('login/',views.LoginView.as_view(),name='user_login'),
    path('logout/',views.LogoutView.as_view(),name='user_logout'),
]
