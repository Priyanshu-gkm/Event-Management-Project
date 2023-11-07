from django.urls import path
from events_tickets import views

urlpatterns = [
    path("", views.WishlistLCView.as_view(), name="LC-wishlist"),
    path("<int:pk>/", views.WishlistDeleteView.as_view(), name="D-wishlist"),
]
