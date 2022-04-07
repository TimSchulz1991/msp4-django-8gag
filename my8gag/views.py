from django.shortcuts import render, redirect
from .forms import PostForm
from .models import Post, Topic, Comment, Profile


# Create your views here.
def home(request):
    posts = Post.objects.all()
    context = {'posts': posts}
    return render(request, 'my8gag/feed.html', context)


def postView(request, pk):
    post = Post.objects.get(id=pk)
    context = {'post': post}
    return render(request, 'my8gag/post_view.html', context)


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


def deletePost(request, pk):
    post = Post.objects.get(id=pk)
    if request.method == "POST":
        post.delete()
        return redirect('home')
    
    context = {'post': post}
    return render(request, 'my8gag/post_delete.html', context)