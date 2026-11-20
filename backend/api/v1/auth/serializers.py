from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


def validate_user_password(password, user=None):
    try:
        validate_password(password, user=user)
    except DjangoValidationError as error:
        raise serializers.ValidationError(error.messages) from error


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    confirmPassword = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "password",
            "confirmPassword",
        ]

    def validate_email(self, value):
        value = value.strip().lower()
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists.")
        return value

    def validate(self, attrs):
        if attrs["password"] != attrs["confirmPassword"]:
            raise serializers.ValidationError({"confirmPassword": "Passwords do not match."})
        validate_user_password(attrs["password"])
        return attrs

    def create(self, validated_data):
        validated_data.pop("confirmPassword")
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
        )
        if hasattr(user, "role"):
            user.role = "student"
            user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get("email", "").strip()
        password = attrs.get("password")

        user = User.objects.filter(email__iexact=email).first()

        if not user or not user.is_active or not user.check_password(password):
            raise AuthenticationFailed("Invalid email or password.")

        return self.get_login_data(user)

    @staticmethod
    def get_login_data(user):
        refresh = RefreshToken.for_user(user)

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": {
                "id": str(user.id),
                "username": user.username,
                "email": user.email,
                "role": getattr(user, "role", "student"),
                "first_name": user.first_name,
                "last_name": user.last_name,
                "is_staff": user.is_staff,
                "is_superuser": user.is_superuser,
                "is_admin": user.is_staff or user.is_superuser or user.role == "admin",
            },
        }


class AdminLoginSerializer(LoginSerializer):
    def validate(self, attrs):
        login_data = super().validate(attrs)
        user = User.objects.filter(email__iexact=attrs["email"].strip()).first()

        if not (user.is_staff or user.is_superuser or user.role == "admin"):
            raise AuthenticationFailed("Invalid email or password.")

        return login_data


class UserSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    password = serializers.CharField(
        write_only=True,
        required=False,
        min_length=8
    )

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
            "role",
            "is_active",
            "date_joined",
        ]
        read_only_fields = ["id", "date_joined"]

    def get_id(self, obj) -> str:
        return str(obj.id)

    def validate_email(self, value):
        value = value.strip().lower()
        instance = self.instance
        existing_user = User.objects.filter(email=value).first()

        if existing_user and (
            instance is None or str(existing_user.id) != str(instance.id)
        ):
            raise serializers.ValidationError("Email already exists.")

        return value

    # Validate password only when creating a new user
    def validate(self, attrs):
        if self.instance is None and not attrs.get("password"):
            raise serializers.ValidationError({
                "password": "Password is required."
            })

        if attrs.get("password"):
            validate_user_password(attrs["password"], user=self.instance)

        return attrs

    def create(self, validated_data):
        password = validated_data.pop("password")

        return User.objects.create_user(
            password=password,
            **validated_data
        )

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        for field, value in validated_data.items():
            setattr(instance, field, value)
        if password:
            instance.set_password(password)
        instance.save()

        return instance