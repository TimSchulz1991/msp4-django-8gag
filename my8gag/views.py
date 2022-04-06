from django.shortcuts import render, redirect
from .forms import PostForm


# Create your views here.
def home(request):
    return render(request, 'my8gag/feed.html')

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
