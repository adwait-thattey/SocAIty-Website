from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, get_object_or_404, Http404
from django.urls import reverse
from .models import Blog, Tag
from .forms import BlogCreateForm
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
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
        elif sortby == "view":
            blogs = blogs.order_by('-views')
        elif sortby == "old":
            # print(sortby)
            blogs = blogs.order_by('create_date')
    else:
        sortby = "recent"
    tags = Tag.objects.all()
    # TODO Not efficient. Make a normal variable and get from there. Update the normal variables whenever tags update

    # print(blogs)
    return render(request, 'blog/blog_list2.html',
                  {'tags': tags, 'blogs': blogs, "default_profile_pic": default_profile_pic,
                   "selected_tag": ret_selected_tag, "sortby": sortby})


@login_required
def blog_create(request):
    if not request.user.userprofile.blog_create_permission:
        raise Http404('This page does not exist')

    if request.method == 'POST':
        blog_create_form = BlogCreateForm(request.POST, request.FILES)
        if blog_create_form.is_valid():
            blog = blog_create_form.save(commit=False)
            blog.author = request.user
            try:
                blog.save()
                return redirect('blog:blog_detail', request.user, blog.slug)
            except ValidationError as v:
                blog_create_form.add_error('slug', "You have another blog with the same slug url. Please change the slug")

    else:
        blog_create_form = BlogCreateForm()

    return render(request, 'blog/blog_create.html', {'create_form': blog_create_form})


def blog_detail(request, username, slug):
    author = User.objects.get(username=username)
    blog = get_object_or_404(Blog, author=author, slug=slug)
    blog.views += 1  # TODO Change this method of counting views. Not correct
    blog.save()
    editable = False
    if request.user == author:
        editable = True
    context = {
        'blog': blog,
        'editable': editable
    }
    return render(request, 'blog/blog_detail_view.html', context)


@login_required
def blog_edit(request, username, slug):
    author = request.user
    blog = get_object_or_404(Blog, author=author, slug=slug)
    if request.method == 'POST':

        edit_form = BlogCreateForm(request.POST, request.FILES, instance=blog)
        if edit_form.is_valid():
            try:
                blog_instance = edit_form.save()
                return redirect('blog:blog_detail', username, blog_instance.slug)
            except ValidationError as v:
                edit_form.add_error('slug', "You have another blog with the same slug url. Please change the slug")

    else:
        edit_form = BlogCreateForm(instance=blog)
    context = {
        'edit_form': edit_form,
    }
    return render(request, 'blog/blog_edit.html', context)
