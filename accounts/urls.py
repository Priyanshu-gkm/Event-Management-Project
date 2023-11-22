from django.urls import path

from accounts import views

urlpatterns = [
    path("", views.AccountLCAPIView.as_view(), name="LC_account"),
    path("<int:pk>/", views.AccountRUDAPIView.as_view(), name="RUD_account"),
    path(
        "change-password/", views.ChangePasswordView.as_view(), name="change_password"
    ),
    path(
        "forgot-password/", views.ForgotPasswordView.as_view(), name="forgot_password"
    ),
    path(
        "forgot-password/<uuid:token>",
        views.ForgotPasswordView.as_view(),
        name="reset_password",
    ),
]
