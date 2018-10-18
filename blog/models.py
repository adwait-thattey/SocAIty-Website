from django.db import models, IntegrityError
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils import timezone
import datetime
import os


# Create your models here.


class Tag(models.Model):
    tag_name = models.CharField(verbose_name="Tag Name", max_length=15)

    def __str__(self):
        return self.tag_name

    @property
    def blogcount(self):
        return self.blog_set.count()


def validate_blog_file_extension(incoming_file):
    extension = os.path.splitext(incoming_file.name)[1]
    allowed_extensions = ['.md', '.html']
    if extension.lower() not in allowed_extensions:
        raise ValidationError("This file type is not allowed")


def get_blog_upload_path(instance, filename):
    return os.path.join("blogs", str(instance.id), filename)


def get_blog_image_upload_path(instance, filename):
    return os.path.join("blogs", str(instance.id), "images", filename)


class Blog(models.Model):
    title = models.CharField(max_length=50)
    author = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True)
    create_date = models.DateTimeField(verbose_name='Date Published', auto_now_add=True, editable=False)
    upvotes = models.PositiveIntegerField(verbose_name="Upvotes", editable=False, default=0)
    downvotes = models.PositiveIntegerField(verbose_name="Downvotes", editable=False, default=0)
    short_description = models.TextField(blank=True, null=True)
    body = RichTextUploadingField(blank=True, null=True)
    picture = models.ImageField(blank=True, null=True, upload_to=get_blog_image_upload_path)
    slug = models.SlugField(max_length=200)
    tags = models.ManyToManyField(to=Tag, blank=True)

    def __str__(self):
        return str(self.title) + ' : by ' + str(self.author)

    def was_published_recently(self):
        return self.create_date >= timezone.now() - datetime.timedelta(minutes=1)
        # TODO Change this to relevant time duration

    def recount_upvotes(self):
        self.upvotes = self.vote_set.filter(upvote_downvote=1).count()
        self.save()

    def recount_downvotes(self):
        self.downvotes = self.vote_set.filter(upvote_downvote=-1).count()
        self.save()

    def recount_votes(self):
        self.recount_upvotes()
        self.recount_downvotes()

    # TODO Set Cron Job to call recount periodically

    def upvote(self, user):
        vote = Vote(voter=user, blog=self, upvote_downvote=1)
        vote.save()

    def downvote(self, user):
        vote = Vote(voter=user, blog=self, upvote_downvote=-1)
        vote.save()


class Vote(models.Model):
    voter = models.ForeignKey(to=User, on_delete=models.CASCADE)
    blog = models.ForeignKey(to=Blog, on_delete=models.CASCADE)
    vote_time = models.DateTimeField(auto_now=True, editable=False)
    upvote_downvote = models.SmallIntegerField(default=0, validators=[MinValueValidator(-1), MaxValueValidator(1)],
                                               help_text="-1 for downvote, 0 for none, 1 for upvote"
                                               )

    class Meta:
        unique_together = ('voter', 'blog')

    def upvote(self):
        if self.upvote_downvote != 1:
            self.upvote_downvote = 1
            self.save()

            self.blog.upvotes += 1
            self.blog.save()

    def downvote(self):
        if self.upvote_downvote != -1:
            self.upvote_downvote = -1
            self.save()

            self.blog.upvotes -= 1
            self.blog.save()

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        try:
            super().save(*args, **kwargs)
        except IntegrityError:
            vote = Vote.objects.get(voter=self.voter, blog=self.blog)
            vote.delete()
            super().save(*args, *kwargs)


# class BlogMeta(models.Model):
#     blog = models.OneToOneField(to=Blog, on_delete=models.CASCADE)
#
#
# def get_blog_video_upload_path(instance, filename):
#     return os.path.join("blogs", str(instance.blog.id), "videos", filename)
#
#
# def validate_blog_video_file_extension(incoming_file):
#     extension = os.path.splitext(incoming_file.name)[1]
#     allowed_extensions = ['.mp4', '.ogg', '.webm']
#     if extension.lower() not in allowed_extensions:
#         raise ValidationError("This file type is not allowed/supported")
#
#
# class BlogVideo(models.Model):
#     blog = models.ForeignKey(to=BlogMeta, on_delete=models.CASCADE)
#     video = models.FileField(upload_to=get_blog_video_upload_path, validators=[validate_blog_video_file_extension])
#
# def get_blog_audio_upload_path(instance, filename):
#     return os.path.join("blogs", str(instance.blog.id), "audios", filename)
#
#
# def validate_blog_audio_file_extension(incoming_file):
#     extension = os.path.splitext(incoming_file.name)[1]
#     allowed_extensions = ['.mp3', '.wav']
#     if extension.lower() not in allowed_extensions:
#         raise ValidationError("This file type is not allowed/supported")
#
#
# class BlogAudio(models.Model):
#     blog = models.ForeignKey(to=BlogMeta, on_delete=models.CASCADE)
#     audio = models.FileField(upload_to=get_blog_audio_upload_path, validators=[validate_blog_audio_file_extension])
#
#
#
# class BlogImage(models.Model):
#     blog = models.ForeignKey(to=BlogMeta, on_delete=models.CASCADE)
#     image = models.ImageField(upload_to=get_blog_image_upload_path)
#
# def get_blog_other_file_upload_path(instance, filename):
#     return os.path.join("blogs", str(instance.blog.id), "other_files", filename)
#
# class BlogFile(models.Model):
#     blog = models.ForeignKey(to=BlogMeta, on_delete=models.CASCADE)
#     file = models.FileField(upload_to=get_blog_other_file_upload_path)
