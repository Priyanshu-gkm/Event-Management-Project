from rest_framework import serializers

from wishlist.models import Wishlist


class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = "__all__"
        extra_kwargs = {"created_by": {"write_only": True}}
