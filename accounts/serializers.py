from rest_framework import serializers

from Event_Management.accounts.models import Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            "id",
            "email",
            "username",
            "fname",
            "lname",
            "gender",
            "role",
            "is_admin",
            "is_active",
            "is_staff",
            "is_superuser",
            "password",
            "forget_password_token",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
            "forget_password_token": {"write_only": True},
        }

    def create(self, validated_data):
        model = self.Meta.model
        return model.objects.create_user(**validated_data)
