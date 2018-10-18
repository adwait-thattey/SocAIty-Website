from django.contrib import admin

from registration import models

admin.site.register((
    models.UserProfile,
    models.EmailConfirmation,
))