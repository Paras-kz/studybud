from email import message
from email.message import Message
import imp
from multiprocessing import context
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Room, Topics, Messages
from .forms import RoomForm
# Create your views here.
# rooms=[
#     {'id':1, 'name':'Lets learn python'},
#     {'id':2, 'name':'Go design'},
#     {'id':3, 'name':'frontend development'},
# ]
# above is the list containing various dictionories
# context={'rooms':rooms}

def loginPage(request):
    page='login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method=='POST':
        username=request.POST.get('username').lower()
        password=request.POST.get('password')

        try:
            user=User.Objects.get(username=username)
        except:
            messages.error(request,'user does not exist')
            
        user=authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request,'username or password does not exist')

    
    context={'page':page}
    return render(request,'base/login_register.html',context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form=UserCreationForm()
    if request.method=='POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.username=user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request,'An error occoured during registration')

    return render(request,'base/login_register.html',{'form':form})

def home(request):
    q = request.GET.get('q') if request.GET.get('q')!=None else ''
    rooms=Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    topics=Topics.objects.all()
    room_count=rooms.count()
    room_messages=Messages.objects.filter(Q(room__topic__name__icontains=q))

    #y default Model Room will have an id assigned for itself
    context={'roomsk':rooms, 'topics':topics, 
             'room_count':room_count, 'room_messages':room_messages}
    return render(request,'base/home.html', context)
    #it means to go to home.html page 
def room(request,k):
    # room=None
    # for i in rooms:
    #     if i['id']==int(k):
    #         room=i 
            #as rooms was a list of dictionary so here i will be one seperate dictionary
    rooms=Room.objects.get(id=k)
    #as already mentioned models will create id's for themselves
    room_messages=rooms.messages_set.all()
    #in above in messages_set.all , messages is the model name in models.py [many to oe relationship]
    participants=rooms.participants.all()
    #above is many to many relationship
    if request.method=='POST':
        message=Messages.objects.create(
            user=request.user,
            room=rooms,
            body=request.POST.get('body')
        )
        rooms.participants.add(request.user)
        return redirect('room',k=rooms.id)

    context={'roomsk':rooms, 'room_messages':room_messages, 'participants':participants}
    return render(request,'base/room.html',context)

def userProfile(request,pk):
    user=User.objects.get(id=pk)
    roomsk=user.room_set.all()
    room_messages=user.messages_set.all()
    topics=Topics.objects.all()
    context={'user':user,'roomsk':roomsk, 'room_messages':room_messages,'topics':topics}
    return render(request,"base/profile.html",context) #2 go to base/rofile.html with context values

@login_required(login_url='login')
def createRoom(request):
    form=RoomForm

    if request.method=='POST':
        form=RoomForm(request.POST)
        if form.is_valid:
            room=form.save(commit=False)
            room.host=request.user
            form.save()
            return redirect("home")
            #here home is the name of home url which we use instead of its path
        # print(request.POST)
        # this will print the newly submitted data on the terminal as a dictionary

    context={'form':form}
    return render(request,'base/room_form.html',context)

@login_required(login_url='login')
def updateRoom(request,pk):
    room=Room.objects.get(id=pk)
    form=RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse("You are not allowed here !!")

    if request.method=="POST":
        form=RoomForm(request.POST, instance=room)
        if form.is_valid:
            form.save()
            return redirect("home")
    context={'form':form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def deleteRoom(request,pk):
    room=Room.objects.get(id=pk)
    
    if request.user != room.host:
        return HttpResponse("You are not allowed here !!")
    if request.method=='POST':
        room.delete()
        return redirect("home")
    return render(request,'base/delete.html',{'obj':room})

@login_required(login_url='login')
def deleteMessage(request,pk):
    message=Messages.objects.get(id=pk)
    
    if request.user != message.user:
        return HttpResponse("You are not allowed here !!")
    if request.method=='POST':
        message.delete()
        return redirect("home")
    return render(request,'base/delete.html',{'obj':message})
