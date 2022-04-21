from django.shortcuts import render, redirect, reverse
from django.db.models import Q, Count
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseRedirect
from .forms import PostForm, ProfileForm
from .models import Post, Topic, Comment, Profile
from django.contrib.auth.forms import UserCreationForm


def registerView(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('home')
        else:
            messages.error(request, "The registration was not successful")

    context = {'form': form}
    return render(request, 'my8gag/register.html', context)


def home(request):
    q = request.GET.get('q') if request.GET.get('q') is not None else ''
    posts = Post.objects.filter(
        Q(topic__name__icontains=q) |
        Q(title__icontains=q)
    ).annotate(num_comments=Count('comment')).order_by('-created')

    topics = Topic.objects.all()

    context = {'posts': posts, 'topics': topics}
    return render(request, 'my8gag/feed.html', context)


def postView(request, pk):
    post = Post.objects.get(id=pk)
    comments = post.comment_set.all().order_by('-created')
    # to query all comments from the selected post
    topics = Topic.objects.all()

    liked = False
    if post.likes.filter(id=request.user.id).exists():
        liked = True

    if request.method == "POST":
        liked = False
        if post.likes.filter(id=request.user.id).exists():
            liked = True
        try:
            if request.POST.get('body') == '':
                messages.error(
                    request, "Make sure to write something!")
            else:
                comment = Comment.objects.create(
                    author=request.user,
                    post=post,
                    body=request.POST.get('body')
                )
                messages.success(
                        request, 'Your comment was created successfully!')
        except: 
            pass
        return redirect('post_view', pk=post.id)

    context = {'post': post, 'comments': comments,
               'topics': topics, 'liked': liked}
    return render(request, 'my8gag/post_view.html', context)


def postLike(request, pk):
    post = Post.objects.get(id=pk)

    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return HttpResponseRedirect(reverse('post_view', args=[str(pk)]))


@login_required(login_url='login')
def createPost(request):
    form = PostForm()

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        # request.FILES necessary so that file is submitted
        # also required to add enctype to the form
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            try:
                post.save()
                messages.success(
                    request, 'Your post was created successfully!')
                return redirect('home')
            except:
                messages.error(
                    request, "Make sure to upload an image file (PNG/JPG)!")

    context = {'form': form}
    return render(request, 'my8gag/post_form.html', context)


@login_required(login_url='login')
def deletePost(request, pk):
    text_type = 'post'
    try:
        post = Post.objects.get(id=pk)
    except Post.DoesNotExist:
        return redirect('home')

    if request.user != post.author:
        return redirect('home')

    if request.method == "POST":
        post.delete()
        messages.success(request, 'Your post was deleted successfully!')
        return redirect('home')

    context = {'post': post, 'text_type': text_type}
    return render(request, 'my8gag/delete.html', context)


@login_required(login_url='login')
def deleteUser(request, pk):
    text_type = 'user'
    user = User.objects.get(id=pk)

    if user != request.user:
        return redirect('home')

    if request.method == "POST":
        user.delete()
        messages.success(request, 'Your profile was deleted successfully!')
        return redirect('home')

    context = {'user': user, 'text_type': text_type}
    return render(request, 'my8gag/delete.html', context)


@login_required(login_url='login')
def deleteComment(request, pk):
    post_id = request.GET.get('post_id')
    try:
        comment = Comment.objects.get(id=pk)
    except Comment.DoesNotExist:
        return redirect('post_view', pk=post_id)

    # receiving the post_id from line 8 in post_view.html

    if request.user != comment.author:
        return redirect('home')

    if request.method == "POST":
        comment.delete()
        messages.success(request, 'Your comment was deleted successfully!')
        return redirect('post_view', pk=post_id)

    context = {'comment': comment, 'post_id': post_id}
    return render(request, 'my8gag/delete.html', context)


@login_required(login_url='login')
def editProfile(request, pk):
    profile = Profile.objects.get(user_id=pk)
    # it is important to get the user_id, not id of the profile table
    form = ProfileForm(instance=profile)

    if request.user != profile.user:
        return redirect('home')

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            try:
                form.save()
                messages.success(
                    request, 'Your profile was edited successfully!')
                return redirect('home')
            except:
                messages.error(
                    request, "Make sure to upload an image file (PNG/JPG)!")

    context = {'profile': profile, 'form': form}
    return render(request, 'my8gag/edit_profile.html', context)
