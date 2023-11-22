from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import (
    ListCreateAPIView,

    DestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated

from wishlist.models import Wishlist
from wishlist.serializers import WishlistSerializer
from wishlist.custom_permissions import IsWishlistItemOwner




class WishlistLCView(ListCreateAPIView):
    serializer_class = WishlistSerializer
    permission_classes = [IsAuthenticated,IsWishlistItemOwner]
    queryset = Wishlist.objects.all()

    def get_queryset(self):
        if self.request.method == "GET":
            return Wishlist.objects.filter(created_by=self.request.user.id)
        return super().get_queryset()

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated()]
        return super().get_permissions()

    def post(self, request, *args, **kwargs):
        data = request.data
        data["created_by"] = request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class WishlistDeleteView(DestroyAPIView):
    serializer_class = WishlistSerializer
    permission_classes = [IsAuthenticated,IsWishlistItemOwner]
    queryset = Wishlist.objects.all()
