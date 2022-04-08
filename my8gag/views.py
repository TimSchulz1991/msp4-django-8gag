from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import PostForm
from .models import Post, Topic, Comment, Profile
from django.contrib.auth.forms import UserCreationForm


# Create your views here.
def loginView(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('home') 

    if request.method == "POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        # try:
        #     user = User.objects.get(username=username)
        # except:
        #     messages.error(request, "User does not exist")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(
                request, "Credentials do not match any user in our database")

    context = {'page': page}
    return render(request, 'my8gag/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def registerView(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home') 
        else:
            messages.error(request, "The registration was not successful")

    context = {'form': form}
    return render(request, 'my8gag/login_register.html', context)


def home(request):
    q = request.GET.get('q') if request.GET.get('q') is not None else ''
    posts = Post.objects.filter(
        Q(topic__name__icontains=q) |
        Q(title__icontains=q)
    )

    topics = Topic.objects.all()

    context = {'posts': posts, 'topics': topics}
    return render(request, 'my8gag/feed.html', context)


def postView(request, pk):
    post = Post.objects.get(id=pk)
    context = {'post': post}
    return render(request, 'my8gag/post_view.html', context)


@login_required(login_url='login')
def createPost(request):
    form = PostForm()

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        # request.FILES necessary so that file is submitted
        # also required to add enctype to the form
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'my8gag/post_form.html', context)


@login_required(login_url='login')
def deletePost(request, pk):
    post = Post.objects.get(id=pk)

    if request.user != post.author:
        return redirect('home')

    if request.method == "POST":
        post.delete()
        return redirect('home')

    context = {'post': post}
    return render(request, 'my8gag/post_delete.html', context)
