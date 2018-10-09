from django.contrib import admin
from . import models
from embed_video.admin import AdminVideoMixin
# Register your models here.

class MyModelAdmin(AdminVideoMixin, admin.ModelAdmin):
    pass

admin.site.register(models.BlogVideo, MyModelAdmin)

admin.site.register((
                        models.Vote,
                        models.BlogMeta,
                        # models.BlogVideo,
                        models.Blog
                     ))