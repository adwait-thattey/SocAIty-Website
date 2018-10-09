from django.shortcuts import render

from blog.models import BlogVideo

def index(request):
    vid = BlogVideo.objects.all()[0]
    return render(request, 'home/index.html', {"vid":vid})
