from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Blog
from .forms import BlogCreateForm
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required


# Create your views here.
def blog_list(request):
    blog_list = Blog.objects.all()
    return render(request, 'blog/blog_list2.html', {'blogs': blog_list})


@login_required
def blog_create(request):
    if request.method == 'POST':
        form = BlogCreateForm(request.POST)
        if form.is_valid:
            blog = form.save(commit=False)
            blog.save()
            return HttpResponseRedirect(reverse('blog:blog_list'))
    else:
        form = BlogCreateForm()
    return render(request, 'blog/blog_create.html', {'form': form})


def blog_detail(request, username, blog_slug):
    blog = get_object_or_404(Blog, username=username, slug=blog_slug)
    context = {
        'blog': blog,
    }
    return render(request, 'blog/blog_detail.html', context)
