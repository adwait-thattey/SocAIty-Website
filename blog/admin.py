from django.contrib import admin
from .models import Blog
# Register your models here.

class PostAdmin(admin.ModelAdmin):
    search_fields = ('author__username','title')
    prepopulated_fields = {'slug':('title',)}
    date_hierarchy = ('created')

admin.site.register(Blog)
