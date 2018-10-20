"""testing_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.blog_list, name='blog_list'),
    path('blog/create', views.blog_create, name='blog_create'),
    path('blog/<str:username>/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('blog/<str:username>/<slug:slug>/edit', views.blog_edit, name='blog_edit'),

    # path('blog_edit/<str:username>/<slug:blog_slug>/',views.blog_edit,name='blog_edit'),
]
