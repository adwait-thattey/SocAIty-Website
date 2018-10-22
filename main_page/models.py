from django.core.exceptions import ValidationError
from django.db import models
from django.template.defaultfilters import truncatechars


# Create your models here.
def limit_instances(instance, limit):
    model = instance.__class__

    if model.objects.count() >= limit:
        raise ValidationError("Only " + str(
            limit) + " instance of this model is allowed! If you want to create a new instance, please delete the previous ones.")


class Progress(models.Model):
    meetups = models.PositiveIntegerField(verbose_name="Meetups Conducted")
    training_session = models.PositiveIntegerField(verbose_name="Training Sessions Conducted")
    members = models.PositiveIntegerField(verbose_name="Total Members")
    developers = models.PositiveIntegerField(verbose_name="Total Developers")

    def clean(self):
        super().clean()
        limit_instances(self, 1)


class ContactUs(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField(blank=True)
    query_resolved = models.BooleanField(default=False)

    @property
    def truncated_message(self):
        return truncatechars(self.message, 50)