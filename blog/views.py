from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Blog, Tag
from .forms import BlogCreateForm
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from registration.defaults import profile_picture as default_profile_pic


# Create your views here.
def blog_list(request):
    req_tag = request.GET.get("tag", None)
    sortby = request.GET.get("sortby", None)
    if req_tag:
        selected_tag = req_tag.replace('_', ' ')
        blogs = Blog.objects.filter(tags__name=selected_tag)
        if Tag.objects.filter(name=req_tag).exists():
            ret_selected_tag = req_tag
        else:
            ret_selected_tag = None
    else:
        blogs = Blog.objects.all()
        ret_selected_tag = None

    if sortby:
        if sortby == "like":
            blogs = blogs.order_by('-upvotes')
        elif sortby == "old":
            # print(sortby)
            blogs = blogs.order_by('create_date')
    else:
        sortby = "recent"
    tags = Tag.objects.all()
    # TODO Not efficient. Make a normal variable and get from there. Update the normal variables whenever tags update

    # print(blogs)
    return render(request, 'blog/blog_list2.html',
                  {'tags': tags, 'blogs': blogs, "default_profile_pic": default_profile_pic, "selected_tag": ret_selected_tag, "sortby":sortby})


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
