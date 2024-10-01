from django.urls import path

from . import views

app_name = "posts"

urlpatterns = [
    path("", views.post, name="list"),
    path("getposts", views.getposts, name="getposts"),
    # path("getimages", views.getimages, name="getimages"),
    path("getmembers", views.getmembers, name="getmembers"),
    path("getmember/<int:id>", views.getmember, name="getmember"),
    path("update_member_to/<int:id>", views.update_member_to, name="update_member_to"),
    path("member-addres", views.member_address, name="member_address"),
    path("getaddress/<int:id>", views.getaddress, name="getaddress"),
    path("member-data/<int:id>", views.memberdetails, name="memberdetails"),
    path("delete/<int:id>", views.delete_member, name="delete"),
    path("new-post/", views.post_new, name="new-post"),
    path("create-member", views.create_member, name="create-member"),
    # path("users-view", views.users_view, name="users-view"),
    path("new-feed", views.new_feed, name="new-feed"),
    path("get-post/<int:id>", views.post_page, name="post_page"),
    # path("<slug:slug>", views.post_page, name="page"),
    path("delete-post/<int:id>", views.delete_post, name="delete_post"),
]
