from django.urls import path
from . import views

urlpatterns = [

  path('login/',views.login_page,name="login"),
  path('logout',views.logout_page,name="logout"),
  path('register/',views.register_page,name="register"),

  path('', views.home, name='home'),
  path('room/<int:pk>/',views.room, name='room'),
  path('profile/<int:pk>',views.userprofile, name="user_profile"),


  path('create-room/',views.create_room, name="create_room"),
  path('update-room/<int:pk>/',views.update_room, name="update_room"),
  path('delete-room/<int:pk>/',views.delete_Room, name="delete_room"),
  path('delete-message/<int:pk>/',views.delete_message, name="delete_message"),
  path('update-user/',views.update_user, name="update_user"),
  path('topics/',views.topicPage, name="topic_page"),
  path('activity/',views.activitypage, name="activity_page"),

]