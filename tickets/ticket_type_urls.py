from django.urls import path
from tickets import views

urlpatterns = [
    path("", views.TicketTypeLC.as_view(), name="LC-ticket-type"),
    path("<int:pk>/", views.TicketTypeRUD.as_view(), name="RUD-ticket-type"),
]
