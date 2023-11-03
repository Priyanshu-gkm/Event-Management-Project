from django.urls import path
from events_tickets import views

urlpatterns = [
    path("",views.TicketLC.as_view(),name="LC-ticket"),
    path("<int:pk>/",views.TicketRUD.as_view(),name="RUD-ticket"),
]