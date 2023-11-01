from django.urls import path
from accounts import views

urlpatterns = [
   path('', views.AccountLCAPIView.as_view(),name="LC_account"),
    path('<int:pk>/', views.AccountRUDAPIView.as_view(),name='RUD_account'),
]