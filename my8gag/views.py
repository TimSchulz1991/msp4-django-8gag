from django.shortcuts import render


# Create your views here.
def home(request):
    return render(request, 'my8gag/feed.html')

def create_post(request):
    context = {}
    return render(request, 'my8gag/post_form.html', context)
