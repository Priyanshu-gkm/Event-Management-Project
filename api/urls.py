from django.contrib import admin
from django.urls import path , include
from accounts import views

urlpatterns = [
    path("accounts/",include('accounts.urls')),
    path('login/',views.LoginView.as_view(),name='user_login'),
    path('logout/',views.LogoutView.as_view(),name='user_logout'),
    path("events/",include("events_tickets.event_urls")),
    path("ticket-types/",include("events_tickets.ticket_type_urls")),
    path("tickets/",include("events_tickets.ticket_urls")),
]
