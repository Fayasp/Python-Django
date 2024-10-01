from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Address, Members, Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["id", "title", "body", "banner"]


class MemberSerializer(serializers.ModelSerializer):
    posts = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all(), many=True)

    username = serializers.CharField(
        required=True,
        allow_null=False,
        allow_blank=False,
        min_length=5,
        max_length=75,
        error_messages={
            "blank": "please enter the username",
            "null": "Please enter the username",
        },
        validators=[
            UniqueValidator(
                queryset=Members.objects.all(), message="Username already exist"
            )
        ],
    )

    email = serializers.EmailField(
        required=False,
        allow_blank=True,
        allow_null=True,
        error_messages={
            "blank": "Please enter the email",
            "null": "Please enter the email",
        },
        validators=[
            UniqueValidator(
                queryset=Members.objects.all(), message="email already exist"
            )
        ],
    )
    age = serializers.IntegerField(
        required=True,
        allow_null=False,
        min_value=18,
        max_value=60,
        error_messages={
            "null": "please enter the age",
            "max_value": "age must be less than 60",
            "min_value": "age must be greater than 18",
        },
    )

    class Meta:
        model = Members
        fields = ["id", "username", "email", "avatar", "age", "posts"]


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ["member_id", "street", "city", "country"]


class PostCreateSerializer(serializers.ModelSerializer):
    auther = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Post
        fields = ["title", "body", "banner", "auther"]
