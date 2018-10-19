from django.contrib import admin
from .models import Vote, Blog, Tag


# Register your models here.

class BlogAdmin(admin.ModelAdmin):
    search_fields = ('author__username','title')
    # prepopulated_fields = {'slug':('title',)}
    date_hierarchy = ('create_date')

admin.site.register(Blog,BlogAdmin)


class VoteAdmin(admin.ModelAdmin):
    def result(self, obj):
        if obj.upvote_downvote == 1:
            return "upvote"
        elif obj.upvote_downvote == 0:
            return "none"
        elif obj.upvote_downvote == -1:
            return "downvote"
        else:
            raise ValueError("One of the votes has a value other than -1,0,1")

    def username(self, obj):
        return obj.voter.username

    def blog_name(self, obj):
        return obj.blog.title

    list_display = ['username', 'blog_name', 'result']

    list_filter = ['voter', 'blog', 'upvote_downvote']

    search_fields = ['username', 'blog_name']


admin.site.register(Vote,VoteAdmin)

admin.site.register((
    Tag,

))
