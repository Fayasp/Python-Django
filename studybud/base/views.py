from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages  #for flash message
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q  #import to bring logic operation for search
from . models import Room,Topic,Message,User
from .forms import RoomForm, UserForm,MyUserCreationForm
# Create your views here.

# rooms = [
#     {'id': 1, 'name' : 'Lets learn python'},
#     {'id': 2, 'name' : 'Design With me'},
#     {'id': 2, 'name' : 'Frontend Developers'},
# ]

def login_page(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        email = request.POST.get('email')

        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
     
        except:
            messages.error(request, "User Does not exist")

        user = authenticate(request,email=email, password=password)
        if user:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, "User name or password does not exist")

    context ={'page': page}
    return render(request,'base/login_reg.html', context)

def logout_page(request):
    logout(request)
    return redirect('home')
    
def register_page(request):
    form = MyUserCreationForm()
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)  #login the user after register
            return redirect('home')
        else:
            messages.error(request,"An error occured during registration")
    return render(request,'base/login_reg.html',{'form': form})


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''   #to filter the room based on topic here q is getting value from templates
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q) 
    ) 
    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()  #count the room
    room_message = Message.objects.filter(Q(room__topic__name__icontains=q))
    context = {'rooms' :rooms,'topics': topics,'room_count':room_count,'room_message':room_message}
    return render(request,'base/home.html',context)


#room and messages in the room
def room(request,pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()
    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)   #add user into partcipate
        return redirect('room', pk = room.id)
    context = {'room':room,'message': room_messages,'participants': participants,}
    return render(request,'base/room.html',context)


def userprofile(request,pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_message = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user,'rooms':rooms,'room_message':room_message,'topics':topics}
    return render(request, 'base/profile.html',context)

@login_required(login_url='login')
def create_room(request):
    form = RoomForm()
    topics = Topic.objects.all()

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        
        Room.objects.create(
            host=request.user,
            topic = topic,
            name = request.POST.get('name'),
            description=request.POST.get('description')
        )
        # form = RoomForm(request.POST)
        # if form.is_valid():
        #     room = form.save(commit=False)
        #     room.host = request.user
        #     room.save()
        #     return redirect('home')
        
    context = {'form':form,'topics':topics}
    return render(request,'base/room_form.html',context)



#update functionality (to update already created form)
@login_required(login_url='login')
def update_room(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.user != room.host:
        return HttpResponse('You are not allowed here!!!')

    context = {'form':form,'topics':topics,'room':room}
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')
        # form = RoomForm(request.POST, instance=room)
        # if form.is_valid:
        #     form.save()
        #     return redirect('home')

    return render(request,'base/room_form.html', context)

# DELETE Room
@login_required(login_url='login')
def delete_Room(request,pk):
    try:
        room = Room.objects.get(id=pk)
    except:
        messages.error(request, "room Does not exist")
        
    if request.user != room.host:
        return HttpResponse('You are not allowed here!!!')
    if request.method == 'POST':
        room.delete()
        return redirect('home')

    return render(request,'base/delete.html', {'obj': room})


# DELETE Comment
@login_required(login_url='login')
def delete_message(request,pk):

    try:
         message = Message.objects.get(id=pk)
    except:
         messages.error(request, "Message Does not exist")
         
         
    
    if request.user != message.user:
        return HttpResponse('You are not allowed here!!!')
    if request.method == 'POST':
        message.delete()
        return redirect('room',pk=message.room.pk)

    return render(request,'base/delete.html', {'obj': message})



@login_required(login_url='login')
def update_user(request):
    user = request.user
    forms = UserForm(instance=user)
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_profile', pk=user.id)
    return render(request,'base/update_user.html',{'forms': forms})


def topicPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''   #to filter the room based on topic here q is getting value from templates

    topics = Topic.objects.filter(name__icontains=q)
    return render(request,'base/topics.html',{'topics': topics})


def activitypage(request):
    messages = Message.objects.all()
    return render(request,'base/activity.html', {'room_message':messages})
