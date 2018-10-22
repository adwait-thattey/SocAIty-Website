from django.contrib import admin

from .models import Progress, ContactUs

# Register your models here.

admin.site.register(Progress)


class ContactUsAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'query_resolved', 'truncated_message']
    list_filter = ['query_resolved']
    search_fields = ['name', 'email', 'message']


admin.site.register(ContactUs, ContactUsAdmin)
