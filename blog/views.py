from django.shortcuts import render,get_object_or_404,redirect
from django.urls import reverse
from . models import Blog
from .forms import BlogCreateForm
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Create your views here.
def blog_list(request):
    blog_list = Blog.objects.all()
    return render(request,'blog/blog_list.html',{'blogs':blog_list})

@login_required
def blog_create(request):
    if request.method == 'POST':
        form = BlogCreateForm(request.POST)
        if form.is_valid:
            blog=form.save(commit=False)
            blog.save()
            return HttpResponseRedirect(reverse('blog:blog_list'))
    else:
        form = BlogCreateForm()
    return render(request,'blog/blog_create.html',{'form':form})

def blog_detail(request,username,slug):
    author = User.objects.get(username=username)
    blog = get_object_or_404(Blog,author=author,slug=slug)
    context = {
        'blog':blog,
    }
    return render(request,'blog/blog_detail.html',context)

@login_required
def blog_edit(request,username,slug):
    author = User.objects.get(username=username)
    blog = get_object_or_404(Blog,author=author,slug=slug)
    if request.method == 'POST':
        form = BlogCreateForm(data=request.POST,instance=blog)
        if form.is_valid:
            form.save()
            return HttpResponseRedirect(reverse('blog:blog_list'))
    else:
        form = BlogCreateForm(instance=blog)
    context = {
        'form':form,
    }
    return render(request,'blog/blog_edit.html',context)
