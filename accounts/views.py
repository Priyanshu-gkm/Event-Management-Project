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
