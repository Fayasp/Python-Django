from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.db import IntegrityError
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class RegisterUserSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        max_length=75,
        error_messages={
            "blank": "please enter the username",
            "null": "please enter the username",
        },
        validators=[
            UniqueValidator(
                queryset=User.objects.all(), message="Username already exist"
            )
        ],
    )
    password = serializers.CharField(
        min_length=8,
        max_length=30,
        error_messages={
            "blank": "Please enter the password",
            "null": "Please enter the password",
        },
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["confirm_password"] = serializers.CharField(
            min_length=8,
            max_length=30,
            error_messages={
                "blank": "Please enter the password",
                "null": "Please enter the password",
            },
        )

    class Meta:
        model = User
        fields = ["id", "username", "password"]

    def validate(self, attrs: dict):
        password = attrs["password"]
        self.fields.pop("confirm_password")
        confirm_password = attrs.pop("confirm_password", None)
        if password != confirm_password:
            raise serializers.ValidationError(
                {"confirm_password": "Password Not Maching"}
            )

        user = User(**attrs)

        try:
            validate_password(password, user)

        except Exception as e:
            error = serializers.as_serializer_error(e)
            raise serializers.ValidationError(error)
        return attrs

    def create(self, validated_data):
        try:
            user = self.perform_create(validated_data)
        except IntegrityError:
            raise ValueError("Cannot create user")
        return user

    def perform_create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class LoginUserSerializer(serializers.Serializer):

    username = serializers.CharField(style={"input_type": "text"})
    password = serializers.CharField(style={"input_type": "password"})

    def validate(self, attrs):
        return super().validate(attrs)
