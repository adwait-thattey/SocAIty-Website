from django.contrib import admin
from .models import Blog
# Register your models here.

class BlogAdmin(admin.ModelAdmin):
    search_fields = ('author__username','title')
    prepopulated_fields = {'slug':('title',)}
    date_hierarchy = ('create_date')

admin.site.register(Blog,BlogAdmin)
