from pydoc_data.topics import topics
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.db.models import Q
from .forms import DiscussionForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from .models import Discussion ,Topic,Blog
from django.contrib.auth.forms import UserCreationForm
# Create your views here.

# deals with login in a user 
def loginPage(request):
    # checks isf a user is authenticated
    if  request.user.is_authenticated:
        return redirect('home')
#collects user details from the form
    if request.method =="POST":
        username=request.POST.get("username").lower()
       # email=request.POST.get("email")
        password=request.POST.get("password")

        try:
           user=User.objects.get(username==username) 
        except:
            messages.error(request," User does not exist")
        user=authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('home')

        else:
            messages.error(request,"username or password does not exist")
    context={}
    return render(request,'base/login.html')

#logs out a user
def logoutUser(request):
    # uses a function'logout' to log out a user
    logout(request)
    return redirect('home')

#registers a new user into the system
def registerUser(request):
    #uses the django registration form
    form =UserCreationForm
    if request.method =="POST":
        form = UserCreationForm(request.POST)
        #checks if the form is valid
        # if user details are valid it stores the user in the system and login automatically
        if form.is_valid():
            user =form.save(commit =False)
            user.username=user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')

        else:
            # if not valid a flash message is raised
            messages.error(request,"Error occurred during registration")

    return render(request,'base/registration.html',{'form':form})

#deals with the homepage where the blogs are read.
def home(request):
    q= request.GET.get('q') if request.GET.get ('q') !=None else ''
        
    discussion=Discussion.objects.filter(
    Q(topic__name__icontains=q)|
    Q(name__icontains=q)|
    Q(description__icontains=q)
    )
    topics=Topic.objects.all()
    discussion_count=discussion.count()
    room_messages=Blog.objects.filter(Q(discuss__topic__name__icontains=q))
    discussed={'discussion': discussion,'topics':topics, 'discussion_count':discussion_count,'room_messages':room_messages}
    return render(request,'base/home.html',discussed)

def  room(request,primaryKey):
    discuss=Discussion.objects.get(id=primaryKey)
    blog_messages= discuss.blog_set.all()
    participants=discuss.participants.all()
    if request.method=="POST":
        message=Blog.objects.create(
            user=request.user,
            discuss=discuss,
            body=request.POST.get('chat')

        )
        
        discuss.participants.add(request.user)
        return redirect('room',primaryKey=discuss.id)
            
    context={'discuss':discuss,
    'blog_messages':blog_messages,
    'participants':participants,
    }
    return render(request,'base/room.html',context)

def userProfile(request,primaryKey):
    user=User.objects.get(id=primaryKey)
    rooms=user.discussion_set.all()
    topics=Topic.objects.all()
    room_messages=user.blog_set.all()
    context={"user":user,"rooms":rooms,"topics":topics,"room_messages":room_messages}
    return render(request,'base/profile.html',context)
@login_required(login_url='login')
def createRoom(request):
    form=DiscussionForm()
    if request.method=="POST":
        form=DiscussionForm(request.POST)
        if form.is_valid():
            room=form.save(commit=False)
            room.host=request.user
            room.save()
            return redirect('home')


    context={'form':form}
    return render(request,'base/room_form.html',context)
@login_required(login_url='login')
def updateRoom(request,primaryKey):
    discuss=Discussion.objects.get(id=primaryKey)
    form=DiscussionForm(instance=discuss)
    if request.user != discuss.host:
        return HttpResponse("You are not allowed here.Not your discussion!")
    if request.method=='POST':
        form = DiscussionForm(request.POST,instance=discuss)
        if form.is_valid():
            form.save()
            return redirect('home')

    context={'form':form}
    return render(request,'base/room_form.html',context)
@login_required(login_url='login')
def deleteRoom(request,primaryKey):
    discuss=Discussion.objects.get(id=primaryKey)
    if request.user != discuss.host:
        return HttpResponse("You are not allowed here.Not your discussion!")
    if request.method=='POST':
        discuss.delete()
        return redirect('home')
    return render(request,'base/delete.html',{'obj':discuss})

@login_required(login_url='login')
def deleteChat(request,primaryKey):
    chat=Blog.objects.get(id=primaryKey)

    if request.user != chat.user:
        return HttpResponse('you are not allowed to delete that chat. it is not yours')

    if request.method=="POST":
        chat.delete()
        return redirect('home')

    return render(request,'base/delete.html',{'obj':chat})