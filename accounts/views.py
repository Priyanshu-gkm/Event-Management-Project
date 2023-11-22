from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.models import Account
from accounts.serializers import AccountSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated, AllowAny
from accounts.custom_permissions import IsAdminUser, IsSameUser
from django.core.mail import send_mail
from Event_Management.settings import EMAIL_HOST_USER
import uuid


class AccountLCAPIView(ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["username"]

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAdminUser()]
        elif self.request.method == "POST":
            return [AllowAny()]
        return super().get_permissions()


class AccountRUDAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["username"]
    permission_classes = [IsAdminUser | IsSameUser]

    def delete(self, request, pk, *args, **kwargs):
        try:
            user = Account.objects.get(id=pk)
            user.is_active = False
            user.save()
            return Response(
                {"message": "account Deleted successfully"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except:
            return Response(
                {"error": "No account found"}, status=status.HTTP_404_NOT_FOUND
            )


class LoginView(APIView):
    def post(self, request):
        if request.method == "POST":
            username = request.data.get("username")
            password = request.data.get("password")
            user = None
            try:
                user = Account.objects.get(username=username)
            except:
                return Response(
                    {"Error": "User does not exist with this username"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            user = authenticate(username=username, password=password)

            if user:
                token, created = Token.objects.get_or_create(user=user)
                return Response(
                    {"token": token.key, "user_id": user.pk, "email": user.email},
                    status=status.HTTP_200_OK,
                )

            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.auth.delete()  # Delete the user's authentication token
        return Response(
            {"message": "Successfully logged out"}, status=status.HTTP_200_OK
        )


class ChangePasswordView(APIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            current_password = request.data.get("current_password")
            new_password = request.data.get("new_password")
            user = authenticate(
                username=request.user.username, password=current_password
            )
            if user:
                user.set_password(new_password)
                user.save()
                return Response(
                    {"message": "password changed successfully"},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"error": "user does not exist"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ForgotPasswordView(APIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def post(self, request):
        try:
            email = request.data.get("email")
            user = self.queryset.get(email=email)
            if user:
                user.forget_password_token = uuid.uuid4()
                user.save()
                send_mail(
                    subject="Password reset token",
                    message=f"To reset your account password, the token is = {user.forget_password_token} ",
                    from_email=EMAIL_HOST_USER,
                    recipient_list=[user.email],
                )
                return Response(
                    {"message": "Email sent to reset password"},
                    status=status.HTTP_200_OK,
                )
        except Account.DoesNotExist as e:
            return Response(
                {"error": "user does not exist with this email"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def patch(self, request, token):
        try:
            user = self.queryset.get(forget_password_token=token)
            new_password = request.data.get("new_password")
            if user:
                user.set_password(new_password)
                user.forget_password_token = None
                user.save()
                return Response(
                    {"message": "password changed successfully"},
                    status=status.HTTP_200_OK,
                )
        except Account.DoesNotExist as e:
            return Response(
                {"error": "user does not exist with this token"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
