from rest_framework import serializers
from django.contrib.auth import get_user_model
from users.models import UserProfile

User = get_user_model()


# Serializer for UserProfile
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["id", "phone", "user_type"]
        read_only_fields = ["id"]


# Serializer for User
class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(source="userprofile", read_only=True)
    password = serializers.CharField(write_only=True, style={"input_type": "password"})

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
            "profile",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        """Create and return a new user with encrypted password."""
        # Extract profile-related data
        phone = validated_data.pop("phone", None)
        user_type = validated_data.pop("user_type", 1)

        # Create the user
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
        )

        # Create the user profile
        UserProfile.objects.create(user=user, phone=phone, user_type=user_type)

        return user

    def update(self, instance, validated_data):
        """Handle updating user account."""
        if "password" in validated_data:
            password = validated_data.pop("password")
            instance.set_password(password)

        return super().update(instance, validated_data)


# Serializer for authentication token
class AuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField(label="Username")
    password = serializers.CharField(
        label="Password", style={"input_type": "password"}, trim_whitespace=False
    )
