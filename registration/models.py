from django.contrib.auth.models import User
# from django.db.models import signals
from django.db import models
import os.path

from django.dispatch import receiver


def get_user_profile_pic_upload_path(instance, filename):
    return os.path.join("accounts", instance.user.username, "profile_pics", filename)


class EmailConfirmation(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField()

    def __str__(self):
        return self.user.username + " : " + str(self.email_confirmed)


class UserProfile(models.Model):
    DEFAULT_IMG = '/accounts/default/default_profile_pic.jpg'
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    about = models.TextField(null=True)
    profile_pic = models.ImageField(upload_to=get_user_profile_pic_upload_path, default=DEFAULT_IMG, blank=False,
                                    null=False)
    github_url = models.URLField(verbose_name="Github Profile Url", blank=True)

    blog_create_permission = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


@receiver(models.signals.post_save, sender=User)
def set_email_confirmed_false(sender, instance, created, **kwargs):
    if created:
        EmailConfirmation.objects.create(user=instance, email_confirmed=False)

        # Users passsing via oauth don't need to confirm email
        if instance.has_usable_password() is False:
            instance.emailconfirmation.email_confirmed = True

        # Superusers don't need to confirm emails
        elif instance.is_superuser:
            instance.emailconfirmation.email_confirmed = True

        instance.emailconfirmation.save()


@receiver(models.signals.post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        up = UserProfile.objects.create(user=instance)

        up.save()
