import json
import os
import time
from pathlib import Path
from pprint import pprint

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.http import HttpRequest, JsonResponse
from django.shortcuts import HttpResponse, redirect, render

from config.settings import MEDIA_URL

from . import forms
from .forms import MembersForm
from .models import Address, Members, Post
from .serializers import (
    AddressSerializer,
    MemberSerializer,
    PostCreateSerializer,
    PostSerializer,
)

# Create your views here.


def post(request):
    return render(request, "post/post.html")


def getposts(request):
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)
    return JsonResponse({"post": serializer.data})


def getmembers(request):
    username = (
        request.GET.get("username") if request.GET.get("username") != None else ""
    )
    age = request.GET.get("age") if request.GET.get("age") != None else ""

    if age:
        start_value = age.split("_")[0]
        end_value = age.split("_")[1]
    q_obj = Q()

    if username:
        q_obj = Q(username__icontains=username) | Q(email__icontains=username)

    if age:
        q_obj &= Q(age__range=(start_value, end_value))

    # print(q_obj,"q_obj")

    members = Members.objects.filter(q_obj)

    # serilization

    serializer = MemberSerializer(members, many=True)
    return JsonResponse({"members": serializer.data})


def getmember(request, id):
    member = Members.objects.filter(id=id).first()
    serialize = MemberSerializer(member)
    return JsonResponse(serialize.data)


def update_member_to(request: HttpRequest, id: int):
    try:
        member = Members.objects.filter(id=id).first()
    except:
        member = None

    if request.method == "POST":
        if not member:
            return JsonResponse({"details": "no member found"}, status=404)

        payload: dict = json.loads(request.body)
        member.posts.clear()

        serializer = MemberSerializer(member, data=payload)
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)

            return JsonResponse(serializer.data)

        return JsonResponse(serializer.errors, status=400)


def member_address(request: HttpRequest):
    if request.method == "POST":
        payload: dict = json.loads(request.body)

        member = Members.objects.filter(id=payload.get("member").strip()).first()

        if not member:
            return JsonResponse({"detail": "member is not present"}, status=404)

        serializer = AddressSerializer(payload)

        street = payload.get("street").strip()
        city = payload.get("city").strip()
        country = payload.get("country")

        address, _ = Address.objects.get_or_create(member_id=member)
        address.street = street
        address.city = city
        address.country = country
        address.save()
        serializer = AddressSerializer(address)
        return JsonResponse(serializer.data)


def getaddress(request, id):
    address = Address.objects.filter(member_id=id).first()
    if not address:
        return JsonResponse({"detail": "address not found"}, status=404)

    serializer = AddressSerializer(address)
    return JsonResponse(serializer.data)


def new_feed(request: HttpRequest):
    if request.method == "POST":
        payload = request.POST.dict()
        payload["auther"] = request.user.pk

        serilizer = PostCreateSerializer(data=payload)
        if serilizer.is_valid():
            serilizer.save()
            return JsonResponse(serilizer.data, status=201)
        return JsonResponse(serilizer.errors, status=400)

    return render(request, "post/add_feed.html")


def create_member(request: HttpRequest):
    if request.method == "POST":
        payload: dict = json.loads(request.body)
        serializer = MemberSerializer(data=payload)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"message": "User Created"}, status=201)
        return JsonResponse(serializer.errors, status=400)

    posts = Post.objects.all()
    context = {"posts": posts}

    return render(request, "post/user_define.html", context)


def validateEmail(email):
    from django.core.exceptions import ValidationError
    from django.core.validators import validate_email

    try:
        validate_email(email)
        return True
    except ValidationError:
        return False


def memberdetails(request, id):
    if request.method == "POST":
        return JsonResponse({})

    member = Members.objects.filter(id=id).first()
    if member:
        posts = member.posts.all()
        if posts.exists():
            context = {"posts": posts, "member": member}
            return render(request, "post/member.html", context)
        context = {"member": member}
        return render(request, "post/member.html", context)
    return render(
        request, "post/member.html", {"error": "No posts related to this member"}
    )


def delete_member(request, id):
    try:
        member = Members.objects.filter(id=id).first()
    except:
        member = None

    if member:
        member.delete()
        return HttpResponse("Member Deleted")
    return HttpResponse("Member not found")


def post_page(request, id):

    post = Post.objects.filter(id=id).first()
    members = post.members.all()
    context = {"post": post, "members": members}

    # post = Post.objects.get(slug=slug)

    return render(request, "post/post_page.html", context)

    q = request.GET.get("q") if request.GET.get("q") != None else ""


def delete_post(request, id):

    post = Post.objects.get(id=id)
    if post:
        post.delete()
    return redirect("home")


# use authentication  only the person who logged in
def post_new(request):
    if request.method == "POST":
        form = forms.CreatePost(
            request.POST, request.FILES
        )  # FILES added because of adding image
        # save with user
        newpost = form.save(commit=False)
        newpost.auther = request.user
        newpost.save()
        return redirect("posts:list")
    form = forms.CreatePost()
    return render(request, "post/post_new.html", {"form": form})
